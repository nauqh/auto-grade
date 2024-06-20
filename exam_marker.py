from abc import ABC, abstractmethod


class ExamMarkerBase(ABC):
    def __init__(self):
        self.solutions = self.get_solutions()
        self.summary = self.initialize_summary()

    def initialize_summary(self):
        return {
            'Not submitted': [],
            'Incorrect': [],
            'Partial': [],
            'Correct': [],
        }

    @abstractmethod
    def get_solutions(self):
        pass

    @abstractmethod
    def check_multiple(self, submission):
        pass


class M21Marker(ExamMarkerBase):
    def __init__(self):
        super().__init__()
        self.exam_name = "M2.1"

    def get_solutions(self):
        return {
            "1": "A",
            "2": "B",
            "3": "c,e",
            "4": "B",
            "5": "E",
            "6": "A,C",
            "7": "C,D",
            "8": "C"
        }

    def check_multiple(self, submission):

        for i, answer in enumerate(submission, 1):
            solution = self.solutions.get(str(i))
            if not answer:
                self.summary['Not submitted'].append(i)
                continue

            if i in {3, 6, 7}:
                self.__evaluate_special_cases(i, answer, solution)
            else:
                if answer == solution:
                    self.summary['Correct'].append(i)
                else:
                    self.summary['Incorrect'].append(i)

        return self.summary

    def __evaluate_special_cases(self, i, answer, correct_answers):
        correct_parts = [part.upper() for part in correct_answers.split(',')]
        submitted_parts = [part.upper() for part in answer.split(',')]

        if set(submitted_parts) == set(correct_parts):
            self.summary['Correct'].append(i)
        elif set(submitted_parts) & set(correct_parts):
            self.summary['Partial'].append(i)
        else:
            self.summary['Incorrect'].append(i)


class M31Marker(ExamMarkerBase):
    def __init__(self):
        super().__init__()
        self.exam_name = "M3.1"

    def get_solutions(self):
        return {
            "1": "D",
            "2": "A",
            "3": "A",
            "4": "B",
            "5": "B",
            "6": "A",
            "7": "C",
            "8": "A",
            "9": "D",
            "10": "C",
            "11": "A",
            "12": "C"
        }

    def check_multiple(self, submission):
        for i, answer in enumerate(submission, 1):
            solution = self.solutions.get(str(i))
            if not answer:
                self.summary['Not submitted'].append(i)
                continue

            if i >= 10:
                i += 1

            if answer == solution:
                self.summary['Correct'].append(i)
            else:
                self.summary['Incorrect'].append(i)

        return self.summary


class M12Marker(ExamMarkerBase):
    def __init__(self):
        super().__init__()
        self.exam_name = "M1.2"

    def get_solutions(self):
        return {
            "1": "B",
            "2": "B",
            "3": "D",
            "4": ["A", "B"],
            "5": "D",
            "6": ["B", "D"],
            "7": "C",
            "8": "B",
            "9": ["C", "D"],
            "10": "B",
            "11": ["A", "B"],
            "12": ["A", "D"],
            "13": "3",
            "14": "200",
            "15": "B"
        }

    def check_multiple(self, submission):
        for i, answer in enumerate(submission, 1):
            solution = self.solutions.get(str(i))
            if not answer:
                self.summary['Not submitted'].append(i)
                continue

            if (i in {4, 6, 9, 11, 12} and answer in solution) or (answer == solution):
                self.summary['Correct'].append(i)
            else:
                self.summary['Incorrect'].append(i)

        return self.summary


if __name__ == "__main__":
    marker_m21 = M21Marker()
    submission_m21 = ['A', 'B', 'c,e', 'B', 'E', 'A,C', 'C,D', 'C']
    summary_m21 = marker_m21.check_multiple(submission_m21)
    print(summary_m21)

    marker_m31 = M31Marker()
    submission_m31 = ['D', 'A', 'A', 'B', 'B',
                      'A', 'C', 'A', 'D', 'C', 'A', 'C']
    summary_m31 = marker_m31.check_multiple(submission_m31)
    print(summary_m31)

    marker_m12 = M12Marker()
    submission_m12 = ['B', 'B', 'D', 'C', 'D',
                      'B', 'C', 'B', 'C', 'B', 'A', 'A', '3', '200', 'B']
    summary_m12 = marker_m12.check_multiple(submission_m12)
    print(summary_m12)
