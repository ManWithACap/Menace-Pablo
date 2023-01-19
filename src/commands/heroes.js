const { SlashCommandBuilder } = require('discord.js');




module.exports = {
    data: new SlashCommandBuilder()
        .setName('heroes')
        .setDescription('( ͡° ͜ʖ ͡°)'),
    async execute(interaction) {
        await interaction.reply('unfinished command!');
    },
};