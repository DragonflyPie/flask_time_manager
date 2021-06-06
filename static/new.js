let weekdays = () => {
  let week = document.getElementById("week_checkbox");
  let checkbox = document.querySelector("#radioweeek");
  checkbox.addEventListener("change", function (e) {
    let target = e.target;
    switch (target.id) {
      case "radioweek-0":
        week.style.display = "none";
        break;
      case "radioweek-1":
        week.style.display = "block";
        break;
      case "radioweek-2":
        week.style.display = "none";
        break;
    }
  });
};

weekdays();
