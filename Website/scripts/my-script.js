function init() {
    const biscuit = document.getElementById('changeme');
    biscuit.innerText = getUrlParam("age");

    document.getElementById("move").addEventListener("click", next);
}

function getSelection(name)
{
    const elem = document.querySelector(`input[name="${name}"]:checked`);
    return elem ? elem.value : "";
}

function clearSelection(name)
{
    const elem = document.querySelector(`input[name="${name}"]:checked`);
    if (elem)
        elem.checked = false;
}

function getUrlParam(name)
{
    const params = new URLSearchParams(window.location.search);
    return params.has(name) ? params.get(name) : "";
}

init();
getQuestion();