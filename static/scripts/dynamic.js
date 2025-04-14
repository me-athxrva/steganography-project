function loadContent(url) {
    document.getElementById("dynamic").innerHTML = 'Loading...';
    fetch(url)
        .then(response => response.text())
        .then(data => {
            document.getElementById("dynamic").innerHTML = data;
            events();
        })
        .catch(error => console.error('Error loading content:', error));
}