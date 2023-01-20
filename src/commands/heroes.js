const { SlashCommandBuilder } = require('discord.js');
var undici = require("undici");
var heroes = "if you see this, something went horribly wrong";
var heroesList = '';
var counter = 0;

async function getData(){
    var response = await undici.request("https://overfast-api.tekrop.fr/heroes");

    heroes = await response.body.text();

    makeMessage();
}

function makeMessage(){
    var heroesJSON = JSON.parse(heroes);
    
    heroesList = "";

    heroesJSON.forEach(H => heroesList = heroesList + H.name + "\n");
}






module.exports = {
    data: new SlashCommandBuilder()
        .setName('heroes')
        .setDescription('Types out an up-to-date list of Overwatch 2 heroes.'),
    async execute(interaction) {
        await getData().then(() => interaction.reply(heroesList));
    },
};