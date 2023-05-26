$(function () {
  $('#callback-button').click(function (e) {
    e.preventDefault();
    $('.modal9').addClass('modal_active9');
    $('body').addClass('hidden');
  });

  $('.modal__close-button').click(function (e) {
    e.preventDefault();
    $('.modal9').removeClass('modal_active9');
    $('body').removeClass('hidden');
  });

  $('.modal9').mouseup(function (e) {
    let modalContent = $(".modal__content9");
    if (!modalContent.is(e.target) && modalContent.has(e.target).length === 0) {
      $(this).removeClass('modal_active9');
      $('body').removeClass('hidden');
    }
  });
});




$(function () {
  $('#callback-button2').click(function (e) {
    e.preventDefault();
    $('.modal2').addClass('modal_active2');
    $('body').addClass('hidden');
  });

  $('.modal__close-button').click(function (e) {
    e.preventDefault();
    $('.modal2').removeClass('modal_active2');
    $('body').removeClass('hidden');
  });

  $('.modal2').mouseup(function (e) {
    let modalContent = $(".modal__content2");
    if (!modalContent.is(e.target) && modalContent.has(e.target).length === 0) {
      $(this).removeClass('modal_active2');
      $('body').removeClass('hidden');
    }
  });
});






$(function () {
  $('#callback-button3').click(function (e) {
    e.preventDefault();
    $('.modal3').addClass('modal_active3');
    $('body').addClass('hidden');
  });

  $('.modal__close-button').click(function (e) {
    e.preventDefault();
    $('.modal3').removeClass('modal_active3');
    $('body').removeClass('hidden');
  });

  $('.modal3').mouseup(function (e) {
    let modalContent = $(".modal__content3");
    if (!modalContent.is(e.target) && modalContent.has(e.target).length === 0) {
      $(this).removeClass('modal_active3');
      $('body').removeClass('hidden');
    }
  });
});






function downloadFile(url) {
  window.location.href = url;
}


function handleFileSelect(event) {
  const fileInput = event.target;
  const file = fileInput.files[0];

  if (file) {
    const form = document.getElementById('photo-form');
    form.submit();
  }
}


// Функция для обработки изменений в поле ввода имени
function filterFiles() {
  var inputText = document.getElementById("name-input").value.toLowerCase();
  var files = document.getElementsByClassName("towar");
  
  for (var i = 0; i < files.length; i++) {
    var fileName = files[i].getAttribute("data-file-name").toLowerCase();
    
    if (fileName.includes(inputText)) {
      files[i].style.display = "block";
    } else {
      files[i].style.display = "none";
    }
  }
}
  
  // Назначьте функцию filterFiles() на событие "input" поля ввода имени
document.getElementById("name-input").addEventListener("input", filterFiles);


$(document).ready(function() {
  $('.user-dropdown').click(function() {
    $(this).toggleClass('open');
  });
});



function updateDays() {
  var yearSelect = document.getElementById("year");
  var monthSelect = document.getElementById("month");
  var daysSelect = document.getElementById("days");

  var year = parseInt(yearSelect.value);
  var month = parseInt(monthSelect.value);

  // Получаем количество дней в выбранном месяце и году
  var daysInMonth = new Date(year, month, 0).getDate();

  // Удаляем все текущие варианты выбора во втором <select>
  while (daysSelect.options.length > 0) {
    daysSelect.options.remove(0);
  }

  // Добавляем новые варианты выбора во второй <select>
  for (var i = 1; i <= daysInMonth; i++) {
    var option = document.createElement("option");
    option.text = i;
    option.value = i;
    daysSelect.add(option);
  }
}





