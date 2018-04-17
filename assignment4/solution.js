/*jshint esversion: 6 */
class Gambler {
    // requirement #1
    constructor(url, token) {
        this.url = url;
        this.token = token;
        this.betAmount = 0;
        this.session = "nothing... yet";
        this.money = 0;
        this.game = "... also nothing";
        this.hitted = false;
        
        // requirement #6 (part of)
        document.getElementsByName("stand")[0].disabled = true;
        document.getElementsByName("hit")[0].disabled = true;
        document.getElementsByName("double_down")[0].disabled = true;
        document.getElementsByName("surrender")[0].disabled = true;
        
        // requirement #2
        fetch(url)
            .then(function(response) {
            return response.text();
        })
            .then(function(helloMessage) {
            console.log(helloMessage);
        });
        
        // requirement #3
        this.getSession(this.url+"sit", "token="+encodeURIComponent(this.token));
    }
    getSession(url, data) {
        this.postData2(url, data)
            .then(data => {
                console.log(JSON.stringify(data));
                this.money = data.money;
                this.session = data.session;
                if (data.game) {
                    this.game = data.game;
                    document.getElementsByName("stand")[0].disabled = false;
                    document.getElementsByName("hit")[0].disabled = false;
                    document.getElementsByName("double_down")[0].disabled = false;
                    // checking if player has pressed the hit button
                    if (this.hitted == false) {
                        document.getElementsByName("surrender")[0].disabled = false;
                    }
                }
                if (data.last_game) {
                    // setting the hit boolean
                    this.hitted = false;
                    
                    // setting elements only available after a game's completion
                    this.game = data.last_game;
                    document.getElementsByName("result")[0].textContent=this.game.result;
                    document.getElementsByName("won")[0].textContent=this.game.won;
                    
                    // disabling some buttons
                    document.getElementsByName("stand")[0].disabled = true;
                    document.getElementsByName("hit")[0].disabled = true;
                    document.getElementsByName("double_down")[0].disabled = true;
                    document.getElementsByName("surrender")[0].disabled = true;
                    
                    // Re-enabling buttons and inputs
                    document.getElementsByName("betButton")[0].disabled = false;
                    document.getElementsByName("bet")[0].disabled = false;
                }
                // setting the elements shared by the game and last_game object
                document.getElementsByName("dealer_hand")[0].textContent=this.game.dealer_hand;
                if (data.game || data.last_game) {
                    for(var i = 0; i < this.game.player_hand.length; i++) {
                        if (this.game.player_hand[i] == 1) {
                            this.game.player_hand[i] = 'A';
                        }
                        if (this.game.player_hand[i] == 11) {
                            this.game.player_hand[i] = 'J';
                        }
                        if (this.game.player_hand[i] == 12) {
                            this.game.player_hand[i] = 'Q';
                        }
                        if (this.game.player_hand[i] == 13) {
                            this.game.player_hand[i] = 'K';
                        }
                    }
                }
                document.getElementsByName("player_hand")[0].textContent=this.game.player_hand;
                document.getElementsByName("last_bet")[0].textContent=this.game.bet;
            
                // setting the session and money elements
                document.getElementsByName("session")[0].textContent=this.session;
                document.getElementsByName("money")[0].textContent=this.money;
            })
            .catch(error => console.error(error));
    }
    postData2(url, data) {
        return fetch(url, {
            body: data,
            cache: 'no-cache',
            headers: {
                'content-type': 'application/x-www-form-urlencoded'
            },
            method: 'POST'
        })
            .then(response => {
                document.getElementsByName("up")[0].textContent=response.statusText;
                return response.json();
        });
    }
    // requirement #4
    bet(amount) {
        // disabling buttons and inputs
        document.getElementsByName("betButton")[0].disabled = true;
        document.getElementsByName("bet")[0].disabled = true;
        
        this.betAmount = amount;
        var betUrl = this.url+this.session+"/bet";
        var betData = "amount="+this.betAmount+"&token="+encodeURIComponent(this.token);
        this.getSession(betUrl, betData);
    }
    stand() {
        var actionUrl = this.url+this.session+"/stand";
        var actionData = "token="+encodeURIComponent(this.token);
        this.getSession(actionUrl, actionData);
    }
    hit() {
        this.hitted = true;
        document.getElementsByName("surrender")[0].disabled = true;
        var actionUrl = this.url+this.session+"/hit";
        var actionData = "token="+encodeURIComponent(this.token);
        this.getSession(actionUrl, actionData);
    }
    double_down() {
        var actionUrl = this.url+this.session+"/double_down";
        var actionData = "token="+encodeURIComponent(this.token);
        this.getSession(actionUrl, actionData);
    }
    surrender() {
        var actionUrl = this.url+this.session+"/surrender";
        var actionData = "token="+encodeURIComponent(this.token);
        this.getSession(actionUrl, actionData);
    }
}