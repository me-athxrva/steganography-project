function events(){
    let r_inp = document.getElementById('r-inp');
    let img_inp = document.getElementById('img-inp');
    let inp_txt = document.getElementById('inp-txt');

    r_inp.value = '';

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

async function sendEncodeRequest(){
    let r_inp = document.getElementById('r-inp');
    const formData = new FormData();
    const enc_val = document.getElementById('enc-val').value;
    const enc_key = document.getElementById('key').value;
    const file = r_inp.files[0];

    if (!file || !enc_val ||!enc_key)  {
        return alert('Incomplete data selected!');
    }

    document.getElementById('encode-btn').disabled = true;
    document.getElementById('encode-btn').textContent = 'Encoding...';

    formData.append('image', file);
    formData.append('text', enc_val);
    formData.append('key', enc_key);

    try {
        const response = await fetch('api/lsb_stego/encode', {
            method: 'POST',
            body: formData,
            credentials: 'include',
        });

        if (!response.ok) {
            document.getElementById('encode-btn').disabled = false;
            document.getElementById('encode-btn').textContent = 'ENCODE';
            return alert(response.status);
        }
        const blob =  await response.blob();
        const imgURL = URL.createObjectURL(blob);

        const imgTag = document.getElementById('resp-img');
        if (imgTag) {
            imgTag.src = imgURL;
        }
        document.getElementById('encode-btn').disabled = false;
        document.getElementById('encode-btn').textContent = 'ENCODE';
        return alert('Image encoded successfully! 🎉');

    } catch (error) {
        document.getElementById('encode-btn').disabled = false;
        document.getElementById('encode-btn').textContent = 'ENCODE';
        return console.log('Error:', error);
    }
}

async function sendDecodeRequest(){
    let r_inp = document.getElementById('r-inp');
    const formData = new FormData();
    const enc_key = document.getElementById('key').value;
    const file = r_inp.files[0];

    if (!file)  {
        return alert('No image selected!');
    }

    document.getElementById('decode-btn').disabled = true;
    document.getElementById('decode-btn').textContent = 'Decoding...';

    formData.append('image', file);
    if (enc_key){
        formData.append('key', enc_key);
    }

    try {
        const response = await fetch('api/lsb_stego/decode', {
            method: 'POST',
            body: formData,
            credentials: 'include',
        });

        if (!response.ok) {
            document.getElementById('decode-btn').disabled = false;
            document.getElementById('decode-btn').textContent = 'DECODE';
            return console.log(response.status);
        }
        const data = await response.json();

        document.getElementById('decode-btn').disabled = false;
        document.getElementById('decode-btn').textContent = 'DECODE';

        return alert(data['data']);

    } catch (error) {
        document.getElementById('decode-btn').disabled = false;
        document.getElementById('decode-btn').textContent = 'DECODE';
        return console.log('Error:', error);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.addEventListener('click', (e) => {
        if (e.target.id === 'decode') {
            e.target.textContent = 'encode';
            e.target.id = 'encode';
            loadContent('/decode');
        } else if (e.target.id === 'encode') {
            e.target.textContent = 'decode';
            e.target.id = 'decode';
            loadContent('/encode');
        }

        if (e.target.id === 'dev') {
            window.location.href = 'https://github.com/me-athxrva';
        }

        if (e.target.id === 'login') {
            window.location.href = '/login';
        }

        if (e.target.id === 'encode-btn') {
            sendEncodeRequest();
        }

        if (e.target.id === 'decode-btn') {
            sendDecodeRequest();
        }
    });

    loadContent('/encode'); // load initial content
});

