var questNum = 0;
var correct = 0;

function getQuestion() {
    const question = document.getElementById('cheese');
    question.innerText = questions[0]["question"];

    const choiceA = document.getElementById('first');
    choiceA.innerText = questions[questNum]["choiceA"];

    const choiceB = document.getElementById('second');
    choiceB.innerText = questions[questNum]["choiceB"];

    const choiceC = document.getElementById('third');
    choiceC.innerText = questions[questNum]["choiceC"];

    const questionNum = document.getElementById('n');
    questionNum.innerText = "Question " + (questNum+1);
}

function init() {
    const biscuit = document.getElementById('changeme');
    biscuit.innerText = getUrlParam("age");

    document.getElementById("move").addEventListener("click", next);
}

function next(event) {
    var y = getSelection("choices");
    var z = questions[questNum]["answer"];
    if (y == z) {
        correct = correct + 1;
    }
    
    questNum = questNum + 1;

    if (questions.length > questNum) {
        getQuestion();
        clearSelection("choices");
    }

    if (questNum == 3) {
        var x = document.getElementById("move");
        x.style.display = "none";
        
        var a = document.getElementById("results");
        a.style.display = "block";

        var b = document.getElementById("quiz");
        b.style.display = "none";

        const finalres = document.getElementById('finalresults');
        if (correct == 0) {
            finalres.innerText = "Bad luck. Your final score was 0.0% (0/3).";
        }
        else if (correct == 1) {
            finalres.innerText = "Bad luck. Your final score was 33.3% (1/3).";
        }
        else if (correct == 2) {
            finalres.innerText = "Not bad. Your final score was 66.7% (2/3).";
        }
        else {
            finalres.innerText = "Impressive. Your final score was 100.0% (3/3).";
        }
        

    }
}

init();
getQuestion();