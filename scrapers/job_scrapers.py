import asyncio
import pandas as pd
import csv
from pathlib import Path
from typing import List
import re
from urllib.parse import urlparse
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode, BrowserConfig
from crawl4ai import DefaultMarkdownGenerator, PruningContentFilter
from jobspy import scrape_jobs
import time


class JobScraper:
    def __init__(self, site_name: str, job_card_selector: str, jd_card_selector: str):
        self.browser_config = BrowserConfig(
            headless=True,
            viewport_height=1200,
            viewport_width=1920,
            user_agent_mode="random",
        )

        self.site_name = site_name
        self.job_card_selector = job_card_selector
        self.jd_card_selector = jd_card_selector

    async def scrape_job_urls(
        self, search_term="python", location="India", results_wanted=50
    ):
        """Scrape job URLs using jobspy"""
        print(
            f"Scraping {results_wanted} job URLs for '{search_term}' in {location}..."
        )

        jobs = scrape_jobs(
            site_name=[self.site_name],
            search_term=search_term,
            location=location,
            results_wanted=results_wanted,
            hours_old=720,  # Last 30 days
        )

        print(f"Found {len(jobs)} jobs")

        # Save initial job data
        jobs.to_csv(
            "jobs_urls.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False
        )

        return jobs["job_url"].dropna().tolist()

    def create_filename_from_url(self, url: str, index: int = None) -> str:
        """Create a safe filename from URL"""
        # Extract job ID or create identifier from URL
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.strip("/").split("/")

        # Try to extract job ID from URL
        job_id = None
        for part in path_parts:
            if part.isdigit() and len(part) > 5:  # Likely a job ID
                job_id = part
                break

        if not job_id and index is not None:
            job_id = f"{self.site_name}_{index:04d}"
        elif not job_id:
            job_id = "unknown_job"

        # Clean filename
        filename = f"job_{job_id}.md"
        return re.sub(r'[<>:"/\\|?*]', "_", filename)

    async def extract_job_card(self, url: str) -> dict:
        """Extract job card from a single Naukri URL"""
        try:
            async with AsyncWebCrawler(config=self.browser_config) as crawler:

                crawler_config = CrawlerRunConfig(
                    cache_mode=CacheMode.BYPASS,
                    # Target the main job description container
                    css_selector=self.job_card_selector,
                    markdown_generator=DefaultMarkdownGenerator(
                        content_filter=PruningContentFilter(
                            threshold=0.3, threshold_type="fixed", min_word_threshold=10
                        ),
                        options={"ignore_links": True, "escape_html": False},
                    ),
                    page_timeout=30000,
                    wait_for="css:" + self.job_card_selector,
                )

                result = await crawler.arun(url=url, config=crawler_config)
                return result

        except Exception as e:
            print(f"Error extracting job description from {url}: {e}")
            return {}

    async def extract_jd_card(self, url: str) -> dict:
        """Extract job description as from a single Naukri URL"""
        try:
            async with AsyncWebCrawler(config=self.browser_config) as crawler:

                crawler_config = CrawlerRunConfig(
                    cache_mode=CacheMode.BYPASS,
                    # Target the main job description container
                    css_selector=self.jd_card_selector,
                    markdown_generator=DefaultMarkdownGenerator(
                        content_filter=PruningContentFilter(
                            threshold=0.3, threshold_type="fixed", min_word_threshold=10
                        ),
                        options={"ignore_links": True, "escape_html": False},
                    ),
                    page_timeout=30000,
                    wait_for="css:" + self.jd_card_selector,
                )

                result = await crawler.arun(url=url, config=crawler_config)
                return result

        except Exception as e:
            print(f"Error extracting job description from {url}: {e}")
            return {}

    def save_individual_markdown(self, job_data: dict, filename: str, output_dir: Path):
        """Save individual job data as markdown file"""
        try:
            markdown_content = f"""# Job Posting

                                    **Source URL:** {job_data['url']}
                                    **Scraped on:** {time.strftime('%Y-%m-%d %H:%M:%S')}
                                    **Status:** {'✅ Success' if job_data['success'] else '❌ Failed'}

                                    ---

                                    ## Job Header Information

                                    {job_data.get('job_header_markdown', 'No header information available')}

                                    ---

                                    ## Job Description

                                    {job_data.get('job_description_markdown', 'No description available')}

                                    ---

                                    ## Metadata

                                    - **Extraction Success:** {job_data['success']}
                                    - **Error (if any):** {job_data.get('error', 'None')}
                                """

            # Write to file
            file_path = output_dir / filename
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(markdown_content)

            print(f"✅ Saved: {filename}")
            return True

        except Exception as e:
            print(f"❌ Failed to save {filename}: {e}")
            return False

    async def scrape_job_batch(
        self, urls: List[str], batch_size: int = 5, delay: float = 2.0
    ) -> List[dict]:
        """Scrape job descriptions in batches to avoid rate limiting"""
        all_results = []
        total_urls = len(urls)

        # Create output directory for markdown files
        markdown_dir = Path("job_markdowns")
        markdown_dir.mkdir(exist_ok=True)

        print(f"Processing {total_urls} URLs in batches of {batch_size}...")
        print(f"Markdown files will be saved to: {markdown_dir.absolute()}")

        for i in range(0, total_urls, batch_size):
            batch_urls = urls[i : i + batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = (total_urls + batch_size - 1) // batch_size

            print(
                f"\nProcessing batch {batch_num}/{total_batches} ({len(batch_urls)} URLs)..."
            )

            # Process batch concurrently
            tasks = []
            for url in batch_urls:
                # Create tasks for both job header and job description extraction
                job_card_task = self.extract_job_card(url)
                jd_card_task = self.extract_jd_card(url)
                tasks.append((url, job_card_task, jd_card_task))

            # Execute all tasks concurrently
            batch_results = []
            for idx, (url, job_card_task, jd_card_task) in enumerate(tasks):
                try:
                    job_card_result, jd_result = await asyncio.gather(
                        job_card_task, jd_card_task
                    )

                    # Combine results
                    combined_result = {
                        "url": url,
                        "success": True,
                        "job_header_markdown": (
                            job_card_result.markdown
                            if hasattr(job_card_result, "markdown")
                            else ""
                        ),
                        "job_description_markdown": (
                            jd_result.markdown if hasattr(jd_result, "markdown") else ""
                        ),
                        "error": None,
                    }

                    # Create filename and save individual markdown file
                    global_index = i + idx + 1
                    filename = self.create_filename_from_url(url, global_index)
                    self.save_individual_markdown(
                        combined_result, filename, markdown_dir
                    )

                    batch_results.append(combined_result)

                except Exception as e:
                    failed_result = {
                        "url": url,
                        "success": False,
                        "job_header_markdown": "",
                        "job_description_markdown": "",
                        "error": str(e),
                    }

                    # Still save failed attempts for debugging
                    global_index = i + idx + 1
                    filename = self.create_filename_from_url(url, global_index)
                    self.save_individual_markdown(failed_result, filename, markdown_dir)

                    batch_results.append(failed_result)

            # Add batch results to all results
            all_results.extend(batch_results)

            # Progress update
            successful = sum(1 for r in batch_results if r.get("success", False))
            print(
                f"Batch {batch_num} completed: {successful}/{len(batch_urls)} successful"
            )

            # Delay between batches to be respectful
            if i + batch_size < total_urls:
                print(f"Waiting {delay} seconds before next batch...")
                await asyncio.sleep(delay)

        return all_results

    def save_results(
        self, results: List[dict], output_file: str = "job_descriptions.csv"
    ):
        """Save all results to a markdown file"""
        # List all created markdown files
        markdown_dir = Path("job_markdowns")
        if markdown_dir.exists():
            md_files = list(markdown_dir.glob("*.md"))
            print(f"Created {len(md_files)} markdown files:")
            for md_file in sorted(md_files):
                print(f"  - {md_file.name}")


async def main():
    """Main function to run the complete job scraping pipeline"""
    glassdoor_scraper = JobScraper(
        site_name="glassdoor",
        job_card_selector=".JobDetails_jobDetailsHeaderWrapper__JlXWG",
        jd_card_selector=".JobDetails_jobDescription__uW_fK",
    )

    naukri_scraper = JobScraper(
        site_name="naukri",
        job_card_selector=".styles_job-header-container___0wLZ",
        jd_card_selector=".styles_job-desc-container__txpYf",
    )

    try:
        # Step 1: Get job URLs
        print("=== Step 1: Scraping Job URLs ===")
        job_urls = await glassdoor_scraper.scrape_job_urls(
            search_term="python", location="Bangalore", results_wanted=3
        )

        if not job_urls:
            print("No job URLs found. Exiting.")
            return

        print(f"Found {len(job_urls)} job URLs to process")

        print("\n=== Step 2: Extracting Job Descriptions ===")
        results = await glassdoor_scraper.scrape_job_batch(
            urls=job_urls,
            batch_size=3,  # Small batch size to be respectful
            delay=3.0,  # 3 second delay between batches
        )

        print("\n=== Step 3: Saving Results ===")
        glassdoor_scraper.save_results(results)

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    # Run the scraper
    asyncio.run(main())
