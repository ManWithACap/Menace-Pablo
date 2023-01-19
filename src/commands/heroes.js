const { SlashCommandBuilder } = require('discord.js');
var undici = require("undici");
var heroes = "if you see this, something went horribly wrong";

async function requestData(){
    var response = await undici.request("https://overfast-api.tekrop.fr/heroes");

    heroes = await response.body.text();

}






module.exports = {
    data: new SlashCommandBuilder()
        .setName('heroes')
        .setDescription('Types out an up-to-date list of Overwatch 2 heroes.'),
    async execute(interaction) {
        await requestData().then(() => interaction.reply({ files: [JSON.parse(heroes)[0].portrait]}));
    },
};