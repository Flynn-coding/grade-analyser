from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    try:
        assignments_df = pd.read_csv(file)
        
        # Processing as per previous script
        assignments_df['Grade'] = pd.to_numeric(assignments_df['Grade'], errors='coerce')
        assignments_df = assignments_df.dropna(subset=['Grade'])
        
        # Calculate average grades for each semester per subject
        semester_averages = assignments_df.groupby(['Subject', 'Semester'])['Grade'].mean().reset_index()
        semester_averages = semester_averages.rename(columns={'Grade': 'Average Semester Grade'})

        # Calculate overall grade per subject
        overall_grades = semester_averages.groupby('Subject')['Average Semester Grade'].mean().reset_index()
        overall_grades = overall_grades.rename(columns={'Average Semester Grade': 'Overall Grade'})

        result = {
            "semester_averages": semester_averages.to_dict(orient="records"),
            "overall_grades": overall_grades.to_dict(orient="records")
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
