// date and time pickers

flatpickr(".flatpickr1", {
  disableMobile: "true",
  allowInput: true,
  altInput: true,
  altFormat: "F j, Y",
  dateFormat: "Y-m-d",
  minDate: "today",
  defaultDate: null,
});

flatpickr(".flatpickr2", {
  disableMobile: "true",
  defaultDate: null,
  enableTime: false,
  dateFormat: "Y-m-d",
  onChange: function (selectedDates, dateStr, instance) {
    $("#datepicker").submit();
  },
});

flatpickr(".flatpickr3", {
  disableMobile: "true",
  allowInput: true,
  enableTime: true,
  noCalendar: true,
  dateFormat: "H:i",
  time_24hr: true,
  defaultDate: "12:00",
});
