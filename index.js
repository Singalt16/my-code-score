const contextTextarea = document.getElementById("context");
const codeTextarea = document.getElementById("code");
const modal = document.getElementById("modal");
const gradeDisplay = document.getElementById("grade");
const gradeExplanationDisplay = document.getElementById("grade-explanation");

function getGrade() {
  const context = contextTextarea.value;
  const code = codeTextarea.value;

  fetch("http://127.0.0.1:5000/get_grade", {
    method: "POST",
    body: JSON.stringify({ code, context }),
    headers: { "Content-Type": "application/json" },
  })
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
      openModal(data.grade, data.explanation);
    });
}

function openModal(grade, explanation) {
  console.log(grade, explanation);
  gradeDisplay.textContent = grade;
  gradeExplanationDisplay.textContent = explanation;
  modal.style.display = "block";
}

function closeModal() {
  modal.style.display = "none";
}
