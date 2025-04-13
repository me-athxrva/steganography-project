function openResult(){
    let openResult = new gsap.timeline({
        ease: "none"
    })
    openResult.fromTo('#info-container', {
        opacity: 0,
        display: 'none'
    },{
        opacity: 1,
        display: 'flex',
        duration: 0.2
    })
}
function closeResult(){
    let tl = new gsap.timeline({
        ease: "none"
    })
    tl.fromTo('#info-container', {
        opacity: 1,
        display: 'flex'
    },{
        opacity: 0,
        display: 'none',
        duration: 0.2
    })
    document.getElementById('copy-result-btn').disabled = true;
    document.getElementById('download-result-btn').disabled = true;
    document.getElementById('decoded-text-result').style.display = 'none';
    document.getElementById('result-img').style.display = 'none';
}


let close_info = document.getElementById('close-result');
let logo = document.getElementById('logo');

close_info.addEventListener('click', ()=>{
    closeResult();
})