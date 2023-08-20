// Перенаправляет на главную страницу  //
function redirectAfterSec(time, page=null){
    function redirectFunction(){
        window.location.href=page;
    }
    time /= 1000;
    console.log(`time = ${time}`);
    if (!page) {page = '/';}
    setTimeout(redirectFunction, time);
}
/////////////////////////////////////////

///////  Выключает кнопку "конвертировать" и анимирует стрелки при загрузке страницы ///////
function loadFilePage(){
    document.addEventListener('DOMContentLoaded', function () {
        const converterBtn = document.getElementById('converter-btn');
        converterBtn.addEventListener('click', function () {
            converterBtn.setAttribute('disabled', "");
        });
    });
    document.addEventListener('DOMContentLoaded', function () {
        const downloadBtn1 = document.getElementById('download-btn');
        downloadBtn1.removeAttribute('disabled');

        showUpArrow();

        showDownArrow();

        showRightArrow(1.5);
    })
}
////////////////////////////////////////////////////////////////////////////////////////////


// Отображает нижнюю стрелку // 
function showUpArrow(opacity=0) {
    const upArrow = document.getElementById('up-arrow');
    upArrow.style.transition = `opacity ${opacity}s ease-in`;
    upArrow.style.opacity = 1;
}
///////////////////////////////
// Отображает верхнюю стрелку // 
function showDownArrow(opacity=0) {
    const downArrow = document.getElementById('down-arrow');
    downArrow.style.transition = `opacity ${opacity}s ease-in`;
    downArrow.style.opacity = 1;
}
///////////////////////////////
// Отображает горизонтальную стрелку // 
function showRightArrow(opacity=0) {
    const rightArrow = document.getElementById('right-arrow');
    rightArrow.style.transition = `opacity ${opacity}s ease-in`;
    rightArrow.style.opacity = 1;
}
///////////////////////////////