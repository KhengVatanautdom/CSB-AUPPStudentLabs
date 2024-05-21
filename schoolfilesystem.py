import csv
from types import new_class
import pandas as pd
from urllib.request import urlopen
from datetime import datetime
import os

class SchoolAssessmentAnalyzer:
    def __init__(self):
        self.data = pd.DataFrame()
        self.web_data = ""

    def process_file(self, file_path):
        if not os.path.exists(file_path):
            print(f"The file {file_path} does not exist.")
            return False
        
        if file_path.endswith('all_semester.csv'):
            self.data = pd.read_csv(file_path)
            self.data['Average'] = self.data[['INF 652', 'CSC 241', 'ITM 101', 'ITM 371', 'COSC 201']].mean(axis=1)
        else:
            print("Wrong file format.")
            return False
        return True
    
    def fetch_web_data(self, file_path, student_name):
        self.web_data = "No web data available"
        
        if not os.path.exists(file_path):
            print(f"The file {file_path} does not exist.")
            return False
        
        if file_path.endswith('.csv'):
            web_data_df = pd.read_csv(file_path)
            column_name = 'Name'  
            if column_name in web_data_df.columns:
                student_row = web_data_df.loc[web_data_df[column_name] == student_name]
                if not student_row.empty and 'Time Spent' in web_data_df.columns:
                    self.web_data = student_row['Time Spent'].iloc[0]
                return True
            else:
                print(f"The column {column_name} does not exist in the file.")
                return False
        else:
            print("Wrong file format.")
            return False

    def student_web_data_insights(self):
        actual_time_spent = self.web_data
        return f"Actual time spent on web resources: {actual_time_spent} minutes"



    def analyze_content(self):
        if self.data.empty:
            print("No data to analyze.")
            return {}
    def analyze_student(self, student_name):
        if self.data.empty:
            print("No data to analyze.")
            return {}

        if student_name not in self.data['Name'].values:
            print(f"No data found for student: {student_name}")
            return {}

        student_data = self.data[self.data['Name'] == student_name]
        student_performance = self._calculate_student_performance(student_data)
        student_subject_analysis = self._student_subject_wise_analysis(student_data)
        
        student_web_data_insights = self.student_web_data_insights()
        overall_performance = self.calculate_overall_performance()
        top_class = self.determine_top_class()
        notable_observations = self.student_notable_observations()
        recommendations = self.student_generate_recommendations()

        student_report = {
            'student_performance': student_performance,
            'student_subject_analysis': student_subject_analysis,
            'student_web_data_insights': student_web_data_insights,
            'overall_performance': overall_performance,
            'top_class': top_class,
            'student_notable_observations': notable_observations,
            'recommendations': recommendations
        }
        return student_report

    def generate_student_summary(self, student_report, student_name):
        if not student_report:
            print("No report to generate summary from.")
            return
        subject_analysis_section = ""
        for subject, details in student_report['student_subject_analysis'].items():
            subject_analysis_section += f"   - {subject}: Score: {details['score']}\n"

        summary = f"""

-------------------------------------------------------------------------------


School Assessment Summary Report for {student_name}:

1. Overall Performance:
   - Average score: {student_report['student_performance']['average_score']}
   - Grade: {student_report['student_performance']['grade']}
   - Top-performing semester: {student_report['student_performance']['top_class']}

2. Subject-wise Analysis:
{subject_analysis_section}
Best-performing class: {student_report['student_performance']['best_subject']}

3. Notable Observations:
   -{student_report['student_performance']['best_subject']} shows a significant potential.

4. Web Data Insights:
   -Time spent: {student_report['student_web_data_insights']}

5. Recommendations:
   -The lowest performing class is {student_report['student_performance']['lowest_subject']}, you should focus on this class. 

Report generated on: {datetime.now().date()}
"""
        print(summary)

    def _calculate_student_performance(self, student_data):
        subject_scores = student_data.iloc[0][['INF 652', 'CSC 241', 'ITM 101', 'ITM 371', 'COSC 201']]
        best_subject = subject_scores.idxmax()
        lowest_subject = subject_scores.idxmin()
        avg_score = subject_scores.mean() 
        grade = self._determine_grade(avg_score)
        top_class = self.data.groupby('Semester')['Average'].mean().idxmax()

        return {
            'average_score': round(avg_score, 2),
            'grade': grade,
            'top_class': top_class,
            'best_subject': best_subject,
            'lowest_subject': lowest_subject
        }
    def _determine_grade(self, avg_score):
        if avg_score > 89:
            return 'A'
        elif avg_score > 79:
            return 'B'
        elif avg_score > 69:
            return 'C'
        elif avg_score > 59:
            return 'D'
        elif avg_score > 49:
            return 'F'
        else:
            return 'F' 

    def _student_subject_wise_analysis(self, student_data):
        analysis = {}
        for subject in ['INF 652', 'CSC 241', 'ITM 101', 'ITM 371', 'COSC 201']:
            score = student_data[subject].iloc[0]
            analysis[subject] = {'score': score,}
        return analysis
        

    def student_notable_observations(self):
        notable_students = self.data.loc[self.data['Average'] > 90, 'Name'].tolist()
        return f"Students with average more than 90z% of total scores: {', '.join(notable_students)}"

    def student_web_data_insights(self):
        return self.web_data

    def student_generate_recommendations(self):
        underperforming_students = self.data.loc[self.data['Average'] < 80, 'Name'].tolist()
        if not underperforming_students:
            return "No underperforming students."
        else:
            return f"Consider additional support for students: {', '.join(underperforming_students)}"

    def calculate_overall_performance(self):
        return {'average_score': self.data['Average'].mean(), }

    def determine_top_class(self):
        return 

# Example usage
if __name__ == "__main__":
    analyzer = SchoolAssessmentAnalyzer()
    file_path = 'all_semester.csv'
    
    if analyzer.process_file(file_path):
        student_name = input("Enter the name of the student: ")
        if analyzer.fetch_web_data('web.csv', student_name):  
            student_report = analyzer.analyze_student(student_name)
            analyzer.generate_student_summary(student_report, student_name)
