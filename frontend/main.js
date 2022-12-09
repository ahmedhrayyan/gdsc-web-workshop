const tasksList = document.getElementById("tasksId");
const loading = document.getElementById("loading");
const dialog = document.getElementById("addTaskDialog");
const showDialog = document.getElementById("showDialog");
const cancelDialog = document.getElementById("cancelDialog");
const addForm = document.getElementById("addForm");

const API_ROOT = "http://localhost:5000";

// API calls
async function getTasks() {
  const res = await fetch(API_ROOT + "/api/tasks");
  const data = await res.json();
  return data;
}

async function addTask(content) {
  const res = await fetch(API_ROOT + "/api/tasks", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ content: content }),
  });
  const data = await res.json();
  return data;
}
// End API calls

// handle open dialog
showDialog.addEventListener("click", () => {
  dialog.showModal();
});

// handle close dialog
cancelDialog.addEventListener("click", () => {
  dialog.close();
});

// handle form submit (adding task)
addForm.addEventListener("submit", async (evt) => {
  evt.preventDefault(); // prevent default behavior (page reload)
  const formData = new FormData(addForm); // get form data
  const content = formData.get("content");
  const data = await addTask(content); // add task to database and get response
  // put the new task in the DOM (html)
  renderTask(data.task)
  // close dialog after adding the task
  dialog.close();
});

function renderTask(task) {
  tasksList.innerHTML += `
        <li>
          <h3>${task.content}</h3>
          <br>
          <time>${task.date}</time>
        </li>
  `;
}

function renderAllTasks(tasks) {
  tasks.forEach((task) => renderTask(task));
}

async function init() {
  const data = await getTasks();
  loading.style.display = "none"; // hide loading after getting data
  renderAllTasks(data.data); // put data in the DOM (html)
}

init();
