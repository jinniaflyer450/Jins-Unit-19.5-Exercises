const guesses = new Set();
const $guessForm = $('#guess-form');
const $guessArea = $('#guesses')
const $score = $('#score-value')
let currentScore = 0;
$score.text(`${currentScore}`)

const response = $(function(){
    console.log('Game started');
    setTimeout(async function(){
        console.log('Game ended!');
        const response = await axios.get('/end-game', {'params': {'finalScore': currentScore}});
        return response;
    }, 60000)
})

$guessForm.on('submit', async function(evt){
    evt.preventDefault();
    const guess = $('#guess').val();
    let newResult = '';
    if(guess.length < 3){
        newResult = $('<p>Word must be a string of three or more characters.</p>')
    }
    else if((guesses.has(guess))){
        newResult = $('<p>Word has already been guessed.</p>')
    }
    else{
        guesses.add(guess);
        const response = await axios.get('/guess', {'params': {'guess': $('#guess').val()}});
        newResult = $(`<p>Successfully guessed! Result: ${response.data.result}</p>`);
        if(response.data.result === 'ok'){
            currentScore += guess.length;
            $score.text(`${currentScore}`);
        }
    }
    $guessArea.append(newResult)
})

//https://api.jquery.com/ready/ Got advice about using "ready" here.

//https://api.jquery.com/append/ Got some help with append here.