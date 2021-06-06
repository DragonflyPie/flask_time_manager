flatpickr(".flatpickr", {
  altInput: true,
  enableTime: true,
  time_24hr: true,
  altFormat: "F j, Y H:i",
  dateFormat: "U",
  minDate: "today",
  defaultDate: null,
});

flatpickr(".flatpickr2", {
  defaultDate: null,
  dateFormat: "Y-m-d",
  onChange: function (selectedDates, dateStr, instance) {
    $("#datepicker").submit();
  },
});
