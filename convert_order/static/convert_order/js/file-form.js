//////////////// 
document.addEventListener('DOMContentLoaded', function () {
    const cookiePopup = document.getElementById('cookie-popup');
    const cookieConfirmButton = document.getElementById('cookie-confirm');

    // Проверяем, была ли сохранена метка в локальном хранилище
    const isCookieConfirmed = localStorage.getItem('cookieConfirmed');

    if (isCookieConfirmed) {
        // Если метка есть, скрываем форму
        cookiePopup.style.display = 'none';
    } else {
        // Добавляем обработчик события нажатия на кнопку "Согласиться"
        cookieConfirmButton.addEventListener('click', function () {
            // Деактивируем форму
            cookiePopup.style.display = 'none';
            // Сохраняем метку в локальное хранилище
            localStorage.setItem('cookieConfirmed', true);
        });
    }
});



// File form

function highlightDropZone(event) {
    event.preventDefault();
    this.classList.add('drop');
}

function unHighlightDropZone(event) {
    event.preventDefault();
    this.classList.remove('drop');
}

function addFile1(name) {
    const addLogo_1 = document.getElementById('add-file-1');
    const addTitle_1 = document.getElementById('add-file-title-1');

    addLogo_1.style.display = 'none';
    addTitle_1.innerText = name;

    isFile1 = true;

    showUpArrow();

    if(isFile1 && isFile2){
        converterBtn.removeAttribute('disabled');
    }
}

function addFile2(name) {
    const addLogo_2 = document.getElementById('add-file-2');
    const addTitle_2 = document.getElementById('add-file-title-2');

    addLogo_2.style.display = 'none';
    addTitle_2.innerText = name;

    isFile2 = true;

    showDownArrow();

    if(isFile1 && isFile2){
        converterBtn.removeAttribute('disabled');
    }
}

function enableDownload() {
    downloadBtn.removeAttribute('disabled');

    showRightArrow();
}

function showPopup1() {
    popup1.style.display = 'block';
}

function hidePopup1() {
    popup1.style.display = 'none';
}

function showPopup2() {
    popup2.style.display = 'block';
}

function hidePopup2() {
    popup2.style.display = 'none';
}

function showUpArrow() {
    const upArrow = document.getElementById('up-arrow');
    upArrow.style.transition = 'opacity 0.5s ease-in';
    upArrow.style.opacity = 1;
}

function showDownArrow() {
    const downArrow = document.getElementById('down-arrow');
    downArrow.style.transition = 'opacity 0.5s ease-in';
    downArrow.style.opacity = 1;
}

function showRightArrow() {
    const rightArrow = document.getElementById('right-arrow');
    rightArrow.style.transition = 'opacity 0.5s ease-in';
    rightArrow.style.opacity = 1;
}

function closeCookies() {
    cookiePopup.style.display = 'none';
}

const popup1 = document.getElementById('popup-info-1');
const popup2 = document.getElementById('popup-info-2');

const cookiePopup = document.getElementById('cookie-popup');

var isFile1 = false;
var isFile2 = false;

const converterBtn = document.getElementById('converter-btn');
const downloadBtn = document.getElementById('download-btn');
converterBtn.setAttribute('disabled', "");
converterBtn.addEventListener('click', enableDownload);
downloadBtn.setAttribute('disabled', "");

const dropFile_1 = document.getElementById('file-field-1');
const dropFile_2 = document.getElementById('file-field-2');

if (dropFile_1) {
    const fileInput_1 = document.getElementById('file_1');
    fileInput_1.value = null;

    dropFile_1.addEventListener('dragover', highlightDropZone);
    dropFile_1.addEventListener('dragenter', highlightDropZone);
    dropFile_1.addEventListener('dragleave', unHighlightDropZone);
    dropFile_1.addEventListener('drop', (event) => {
        const file_1 = event.dataTransfer.files;
        unHighlightDropZone.call(dropFile_1, event);
        
        fileInput_1.files = file_1;
        addFile1(file_1[0].name);
    });

    fileInput_1.addEventListener('change', (event) => {
        const file_1 = event.target.files;
        addFile1(file_1[0].name);
    })
}

if (dropFile_2) {
    const fileInput_2 = document.getElementById('file_2'); 
    fileInput_2.value = null;

    dropFile_2.addEventListener('dragover', highlightDropZone);
    dropFile_2.addEventListener('dragenter', highlightDropZone);
    dropFile_2.addEventListener('dragleave', unHighlightDropZone);
    dropFile_2.addEventListener('drop', (event) => {
        const file_2 = event.dataTransfer.files;
        unHighlightDropZone.call(dropFile_2, event)

        fileInput_2.files = file_2;
        addFile2(file_2[0].name);
    });

    fileInput_2.addEventListener('change', (event) => {
        const file_2 = event.target.files;
        addFile2(file_2[0].name);
    })
}




