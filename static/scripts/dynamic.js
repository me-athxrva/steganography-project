function loadContent(url) {
    fetch(url)
        .then(response => response.text())
        .then(data => {
            document.getElementById("dynamic").innerHTML = data;
            events();
        })
        .catch(error => console.error('Error loading content:', error));
}