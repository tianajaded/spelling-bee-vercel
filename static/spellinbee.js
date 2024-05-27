// spellinbee.js
function registerPlayers() {
    var player1Name = document.getElementById("player1Name").value;
    var player2Name = document.getElementById("player2Name").value;

    var data = {
        "player1": player1Name,
        "player2": player2Name
    };

    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            if (data.msg) {
                var centerLetter = data.letters.center;
                var outerLetters = data.letters.outer;
                document.getElementById("center").innerText = centerLetter;
                for (var i = 0; i < outerLetters.length; i++) {
                    document.getElementById("outer" + (i + 1)).innerText = outerLetters[i];
                }
                document.getElementById("potentialWords").innerText = `Potential Words: ${data.potential_words}`;
                document.getElementById("game").style.display = "block";
            } else if (data.error) {
                alert(data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("A silly error occurred. Please try again.");
        });
}


function initialTurn() {
    var playerName = document.getElementById("currentPlayerName").value;
    var messageElement = document.getElementById("message");

    messageElement.innerText = "";

    var data = {
        "player": playerName
    };

    fetch('/initial_turn', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to start turn.');
            }
            return response.json();
        })
        .then(data => {
            if (data.msg) {
                messageElement.innerText = data.msg;
                document.getElementById("game").style.display = "block";
                updateScores(data.scores);
                updateRank(data.ranks);
            } else {
                throw new Error(data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            messageElement.innerText = "A nasty error occurred. Please try again.";
            alert(error.message);
        });
}

function updateHoneycomb(letters) {
    document.getElementById("center").innerText = letters.center;
    for (let i = 1; i <= 6; i++) {
        document.getElementById(`outer${i}`).innerText = letters.outer[i - 1];
    }
}

function submitWord() {
    var playerName = document.getElementById("currentPlayerName").value;
    var word = document.getElementById("wordInput").value;
    var messageElement = document.getElementById("message");

    messageElement.innerText = "";

    var data = {
        "player": playerName,
        "word": word
    };

    fetch('/take_turn', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            if (data.msg) {
                messageElement.innerText = data.msg;
                updateScores(data.scores);
            } else if (data.error) {
                messageElement.innerText = data.error;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            messageElement.innerText = "A goofy error occurred. Please try again.";
        });
}

function updateScores(scores) {
    console.log("Received scores:", scores);
    if (scores.player1) {
        document.getElementById("player1Score").innerText = `${scores.player1.name}: ${scores.player1.score} points`;
        document.getElementById("player1Rank").innerText = `Rank: ${scores.player1.rank}`;
    }
    if (scores.player2) {
        document.getElementById("player2Score").innerText = `${scores.player2.name}: ${scores.player2.score} points`;
        document.getElementById("player2Rank").innerText = `Rank: ${scores.player2.rank}`;
    }
}



function updateScores(scores) {
    console.log("Received scores:", scores);
    if (scores.player1) {
        document.getElementById("player1Score").innerText = `${scores.player1.name}: ${scores.player1.score} points`;
        document.getElementById("player1Rank").innerText = `Player 1 Rank: ${scores.player1.rank}`;

    }
    if (scores.player2) {
        document.getElementById("player2Score").innerText = `${scores.player2.name}: ${scores.player2.score} points`;
        document.getElementById("player2Rank").innerText = `Player 2 Rank: ${scores.player2.rank}`;

    }
}
