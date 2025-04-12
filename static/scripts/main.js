let r_inp = document.getElementById('r-inp');
let img_inp = document.getElementById('img-inp');
let inp_txt = document.getElementById('inp-txt');

function fileUpload(){

    img_inp.addEventListener('click',()=>{
        r_inp.click();
    });

    r_inp.addEventListener('change', () => {
        const file = r_inp.files[0];
        if (file.length > 1){
            alert('Please select 1 file at a time!');
            r_inp.value = '';
        }
        if (file && file.type.startsWith('image/')) {
          inp_txt.textContent = `Selected ${file.name}`;
        } else {
          alert('Please select a valid image file.');
          r_inp.value = '';
        }
    });

}

fileUpload();