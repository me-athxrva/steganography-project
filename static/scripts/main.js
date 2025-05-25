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
            alert('Please select 1 file at a time! 😒');
            r_inp.value = '';
        }
        if (file && file.type.startsWith('image/')) {
          inp_txt.textContent = `Selected ${file.name}`;
        } else {
          alert('Please select a valid image file. 😅');
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

    if (enc_key.length==0 || enc_val.length==0) {
        alert('fill up everything dude! 🫠');
        return;
    }

    if (!file || !enc_val ||!enc_key)  {
        return alert('Incomplete data selected! 😅');
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

        if (response.status === 401) {
            alert('Guest trials exhausted. Please login! 😊');
            document.getElementById('encode-btn').disabled = false;
            document.getElementById('encode-btn').textContent = 'ENCODE';
            return;
        }

        if (!response.ok) {
            document.getElementById('encode-btn').disabled = false;
            document.getElementById('encode-btn').textContent = 'ENCODE';
            console.log('Error:', response.status);
            return alert('Internal server error 🤕');
        }
        const blob =  await response.blob();
        const imgURL = URL.createObjectURL(blob);

        const imgTag = document.getElementById('result-img');
        openResult();
        document.getElementById('download-result-btn').disabled = false;
        document.getElementById('result-img').style.display = 'flex';

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
            alert('Unable to decode image, please check your key! 🫣');
            return console.log(response.status);
        }
        const data = await response.json();
        if (data['data']==='Decryption failed!'){
            document.getElementById('decode-btn').disabled = false;
            document.getElementById('decode-btn').textContent = 'DECODE';
            alert('Please check your key! 🫣');
            return;
        }
        openResult();

        document.getElementById('decode-btn').disabled = false;
        document.getElementById('decode-btn').textContent = 'DECODE';
        document.getElementById('copy-result-btn').disabled = false;
        document.getElementById('decoded-text-result').style.display = 'flex';
        document.getElementById('decoded-text-result').textContent = data['data'];

        return;

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
            window.location.href = 'https://atharvadeore.me';
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

        if (e.target.id === 'copy-result-btn') {
            navigator.clipboard.writeText(document.getElementById('decoded-text-result').textContent);
            alert('Text copied to clipboard! 🫡');
        }

        if (e.target.id === 'download-result-btn') {
            const imgElement = document.getElementById('result-img');
            const blobUrl = imgElement.src;

            if (!blobUrl || !blobUrl.startsWith('blob:')) {
                console.error('Invalid blob URL');
                return;
            }

            fetch(blobUrl)
                .then(response => response.blob())
                .then(blob => {
                    const a = document.createElement('a');
                    a.href = URL.createObjectURL(blob);
                    a.download = 'encoded_image.jpg';
                    a.click();

                    URL.revokeObjectURL(a.href);
                })
                .catch(error => {
                    console.error('Error fetching blob:', error);
                });
        }
    });

    loadContent('/encode');
});

