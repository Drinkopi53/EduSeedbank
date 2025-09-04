"""
HTML interactive content generator for EduSeedbank.
Creates interactive educational HTML content.
"""

import os
from typing import List, Dict


class HTMLGenerator:
    """Generates interactive HTML educational content."""

    def __init__(self):
        self.templates_dir = os.path.join(os.path.dirname(__file__), "templates")
        os.makedirs(self.templates_dir, exist_ok=True)

    def create_interactive_page(self, title: str, content: str, 
                              exercises: List[Dict] = None) -> str:
        """
        Create an interactive HTML page with exercises.
        
        Args:
            title: Page title
            content: Main content (HTML format)
            exercises: List of exercise dictionaries
            
        Returns:
            Generated HTML content as string
        """
        exercises = exercises or []
        
        html_content = f"""
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}
        .content {{
            line-height: 1.6;
            color: #333;
        }}
        .exercise {{
            background-color: #ecf0f1;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
        }}
        .question {{
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .options {{
            margin-left: 20px;
        }}
        .option {{
            margin: 5px 0;
        }}
        button {{
            background-color: #3498db;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }}
        button:hover {{
            background-color: #2980b9;
        }}
        .feedback {{
            margin-top: 10px;
            padding: 10px;
            border-radius: 5px;
            display: none;
        }}
        .correct {{
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }}
        .incorrect {{
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <div class="content">
            {content}
        </div>
        
        {''.join(self._generate_exercise_html(i, ex) for i, ex in enumerate(exercises))}
    </div>
    
    <script>
        function checkAnswer(exerciseId, correctAnswer) {{
            const selectedOption = document.querySelector(`input[name="exercise${{exerciseId}}"]:checked`);
            const feedback = document.getElementById(`feedback${{exerciseId}}`);
            
            if (!selectedOption) {{
                feedback.textContent = "Silakan pilih jawaban terlebih dahulu.";
                feedback.className = "feedback incorrect";
                feedback.style.display = "block";
                return;
            }}
            
            if (selectedOption.value === correctAnswer) {{
                feedback.textContent = "Benar! Jawaban Anda tepat.";
                feedback.className = "feedback correct";
            }} else {{
                feedback.textContent = "Jawaban salah. Coba lagi!";
                feedback.className = "feedback incorrect";
            }}
            
            feedback.style.display = "block";
        }}
    </script>
</body>
</html>
        """
        
        return html_content.strip()

    def _generate_exercise_html(self, index: int, exercise: Dict) -> str:
        """Generate HTML for a single exercise."""
        options_html = ""
        for i, option in enumerate(exercise.get("options", [])):
            options_html += f'''
            <div class="option">
                <input type="radio" id="option{index}_{i}" name="exercise{index}" value="{option}">
                <label for="option{index}_{i}">{option}</label>
            </div>'''
        
        return f'''
        <div class="exercise">
            <div class="question">{exercise.get("question", "Pertanyaan tidak tersedia")}</div>
            <div class="options">
                {options_html}
            </div>
            <button onclick="checkAnswer({index}, '{exercise.get("correct_answer", "")}')">Periksa Jawaban</button>
            <div id="feedback{index}" class="feedback"></div>
        </div>'''

    def save_page(self, html_content: str, file_path: str) -> bool:
        """
        Save HTML content to a file.
        
        Args:
            html_content: HTML content to save
            file_path: Path where to save the file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            return True
        except Exception as e:
            print(f"Error saving HTML file: {e}")
            return False