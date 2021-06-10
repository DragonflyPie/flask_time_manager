let weekdays = () => {
  let week = document.getElementById("week_checkbox");
  let datepicker = document.getElementById("datepickr");
  let goal = document.querySelector(".inline_block p");
  let checkbox = document.querySelector("#radioweeek");
  checkbox.addEventListener("change", function (e) {
    let target = e.target;
    switch (target.id) {
      case "radioweek-0":
        week.style.display = "none";
        datepicker.style.display = "block";
        goal.style.display = "none";
        break;
      case "radioweek-1":
        week.style.display = "flex";
        datepicker.style.display = "none";
        goal.style.display = "none";
        break;
      case "radioweek-2":
        week.style.display = "none";
        datepicker.style.display = "block";
        goal.style.display = "flex";
        break;
    }
  });
};

weekdays();
