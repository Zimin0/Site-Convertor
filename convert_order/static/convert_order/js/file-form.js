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
    console.log("addFile1 is running!")
    const addLogo_1 = document.getElementById('add-file-1');
    const addTitle_1 = document.getElementById('add-file-title-1');
    console.log(addTitle_1);  // Должно вывести HTML элемент, а не null

    addLogo_1.style.display = 'none';
    addTitle_1.innerText = name;

    isFile1 = true;

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

    if(isFile1 && isFile2){
        converterBtn.removeAttribute('disabled');
    }
}

function enableDownload() {
    downloadBtn.removeAttribute('disabled');
}

var isFile1 = false;
var isFile2 = false;

const converterBtn = document.getElementById('converter-btn');
const downloadBtn = document.getElementById('download-btn');
converterBtn.setAttribute('disabled', "");
converterBtn.addEventListener('click', enableDownload);


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
