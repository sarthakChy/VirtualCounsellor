class StenCalculator:
    """
    A class to calculate sten scores based on norm tables for different grades and genders.
    Supports grades 9-12 with separate norms for boys and girls.
    """

    def __init__(self):
        self.norms = {
            9: {
                "male": {
                    "CA": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],  # sten 1-10 cutoffs
                    "CL": [0, 8, 13, 17, 21, 26, 30, 34, 38, 43],
                    "MA": [0, 3, 4, 6, 7, 9, 10, 12, 13, 15],
                    "NA": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                    "PM": [0, 5, 10, 13, 17, 21, 24, 27, 30, 33],
                    "RA": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                    "SA": [0, 11, 17, 23, 29, 35, 41, 47, 53, 59],
                    "VA": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                },
                "female": {
                    "CA": [0, 2, 3, 4, 6, 7, 8, 9, 10, 12],
                    "CL": [0, 10, 15, 20, 25, 30, 35, 39, 44, 49],
                    "MA": [0, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    "NA": [0, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    "PM": [0, 8, 13, 17, 21, 26, 30, 34, 39, 43],
                    "RA": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                    "SA": [0, 10, 15, 20, 25, 30, 35, 40, 45, 50],
                    "VA": [0, 2, 3, 4, 6, 7, 8, 9, 10, 12],
                },
            },
            10: {
                "male": {
                    "CA": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                    "CL": [0, 9, 14, 18, 23, 28, 32, 37, 42, 47],
                    "MA": [0, 3, 5, 7, 9, 11, 13, 15, 17, 19],
                    "NA": [0, 2, 3, 4, 5, 6, 8, 10, 11, 12],
                    "PM": [0, 7, 10, 14, 17, 21, 24, 28, 31, 35],
                    "RA": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                    "SA": [0, 12, 18, 24, 31, 37, 43, 49, 55, 61],
                    "VA": [0, 2, 3, 4, 6, 7, 8, 10, 12, 13],
                },
                "female": {
                    "CA": [0, 2, 4, 5, 6, 8, 9, 10, 12, 13],
                    "CL": [0, 10, 16, 21, 26, 32, 37, 42, 47, 53],
                    "MA": [0, 2, 3, 4, 5, 7, 8, 9, 10, 11],
                    "NA": [0, 2, 3, 4, 5, 6, 8, 9, 10, 11],
                    "PM": [0, 8, 13, 17, 21, 26, 30, 34, 39, 43],
                    "RA": [0, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    "SA": [0, 11, 16, 21, 27, 32, 37, 43, 48, 53],
                    "VA": [0, 2, 4, 5, 7, 8, 10, 11, 13, 15],
                },
            },
            11: {
                "male": {
                    "CA": [0, 2, 3, 5, 6, 7, 8, 9, 11, 12],
                    "CL": [0, 10, 15, 20, 25, 30, 35, 40, 45, 50],
                    "MA": [0, 4, 6, 9, 11, 13, 15, 17, 19, 21],
                    "NA": [0, 2, 4, 5, 6, 8, 9, 10, 12, 13],
                    "PM": [0, 7, 11, 15, 19, 22, 26, 30, 34, 38],
                    "RA": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                    "SA": [0, 13, 19, 26, 32, 39, 45, 52, 58, 65],
                    "VA": [0, 3, 4, 6, 7, 9, 10, 12, 14, 16],
                },
                "female": {
                    "CA": [0, 3, 4, 6, 7, 9, 10, 12, 13, 15],
                    "CL": [0, 11, 17, 22, 28, 34, 39, 45, 51, 56],
                    "MA": [0, 3, 4, 6, 7, 8, 9, 10, 12, 13],
                    "NA": [0, 2, 4, 5, 7, 8, 9, 10, 12, 14],
                    "PM": [0, 8, 13, 17, 21, 26, 30, 34, 39, 43],
                    "RA": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                    "SA": [0, 12, 18, 24, 31, 37, 43, 49, 55, 61],
                    "VA": [0, 3, 5, 7, 9, 10, 12, 14, 16, 18],
                },
            },
            12: {
                "male": {
                    "CA": [0, 1, 4, 6, 8, 11, 13, 15, 17, 19],
                    "CL": [0, 10, 16, 21, 26, 31, 36, 42, 47, 52],
                    "MA": [0, 4, 7, 9, 12, 14, 16, 19, 21, 24],
                    "NA": [0, 1, 4, 6, 8, 9, 11, 13, 16, 19],
                    "PM": [0, 8, 12, 16, 19, 23, 27, 31, 35, 39],
                    "RA": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                    "SA": [0, 15, 22, 28, 34, 40, 47, 53, 59, 66],
                    "VA": [0, 1, 4, 7, 10, 13, 16, 18, 21, 22],
                },
                "female": {
                    "CA": [0, 2, 4, 6, 8, 10, 12, 14, 16, 18],
                    "CL": [0, 11, 17, 23, 29, 35, 41, 47, 53, 59],
                    "MA": [0, 3, 5, 6, 8, 10, 11, 13, 15, 17],
                    "NA": [0, 2, 5, 7, 9, 11, 13, 16, 17, 19],
                    "PM": [0, 9, 14, 18, 23, 28, 33, 38, 42, 47],
                    "RA": [0, 2, 3, 4, 5, 6, 7, 8, 9, 11],
                    "SA": [0, 11, 18, 25, 32, 39, 46, 53, 60, 67],
                    "VA": [0, 3, 5, 8, 10, 13, 16, 18, 21, 22],
                },
            },
        }

    def get_sten_score(self, raw_score, ability, grade, gender="male"):
        """
        Convert raw score to sten score based on norms

        Args:
            raw_score: The achieved score
            ability: Test ability code (CA, CL, MA, NA, PM, RA, SA, VA)
            grade: Grade level (9, 10, 11, 12)
            gender: 'male' or 'female'

        Returns:
            Sten score (1-10) or None if invalid input
        """
        if raw_score is None:
            return None

        if grade not in self.norms:
            raise ValueError(
                f"Grade {grade} not supported. Available grades: {list(self.norms.keys())}"
            )

        if gender not in self.norms[grade]:
            raise ValueError(
                f"Gender '{gender}' not supported. Available: {list(self.norms[grade].keys())}"
            )

        if ability not in self.norms[grade][gender]:
            raise ValueError(
                f"Ability '{ability}' not supported. Available: {list(self.norms[grade][gender].keys())}"
            )

        cutoffs = self.norms[grade][gender][ability]

        # Find the appropriate sten score
        for sten in range(10, 0, -1):  # Start from sten 10 and work down
            if raw_score >= cutoffs[sten - 1]:
                return sten

        return 1  # If below all cutoffs, assign sten 1

    def format_results(self, results):
        """
        Format results in a readable way
        """
        formatted = []
        for ability, data in results.items():
            raw = data["raw_score"] if data["raw_score"] is not None else "N/A"
            sten = data["sten_score"] if data["sten_score"] is not None else "N/A"
            formatted.append(f"{ability}: Raw={raw}, Sten={sten}")

        return "\n".join(formatted)

    def parse_score_input(self, score_input):
        """
        Parse score input in format "achieved/total", "achieved", or float.
        Returns the achieved score as integer, or None if invalid.
        """
        if score_input is None:
            return None

        # If it's already numeric
        if isinstance(score_input, (int, float)):
            return int(score_input)

        # Handle strings
        if isinstance(score_input, str):
            score_string = score_input.strip()
            if score_string == "":
                return None

            if "/" in score_string:
                try:
                    achieved, total = score_string.split("/")
                    return int(achieved.strip())
                except (ValueError, IndexError):
                    return None
            else:
                try:
                    return int(score_string)
                except ValueError:
                    return None

        return None

    def calculate_student_stens(self, scores_dict, grade, gender="male"):
        results = {}
        for ability, score_string in scores_dict.items():
            raw_score = self.parse_score_input(score_string)
            sten_score = self.get_sten_score(raw_score, ability, grade, gender)
            results[ability] = {"raw_score": raw_score, "sten_score": sten_score}
        return results


# Example usage and testing
if __name__ == "__main__":
    calculator = StenCalculator()

    # Example from the problem description
    example_scores = {
        "CA": "13/20",
        "CL": "43/72",
        "MA": "",
        "NA": "17/20",
        "PM": "",  # Missing score
        "RA": "",
        "SA": "33/72",
        "VA": "18/24",
    }

    results = calculator.calculate_student_stens(
        example_scores, grade=11, gender="female"
    )

    print("Student Sten Score Results:")
    print("=" * 30)
    print(calculator.format_results(results))

    print("\nSten scores only:")
    sten_only = [
        str(data["sten_score"]) if data["sten_score"] is not None else "N/A"
        for data in results.values()
    ]
    print(", ".join(sten_only))
