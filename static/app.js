const guesses = new Set();
const $guessForm = $('#guess-form');
$guessForm.on('submit', async function(evt){
    evt.preventDefault();
    const guess = $('#guess').val();
    if(guess.length < 3){
        return "Guess must be a string of at least three characters."
    }
    else if((guesses.has(guess))){
        return "Word already guessed."
    }
    else{
        guesses.add(guess);
        const response = await axios.get('/guess', {'params': {'guess': $('#guess').val()}});
        return response;
    }
})
