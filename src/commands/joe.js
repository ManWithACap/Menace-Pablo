const { SlashCommandBuilder } = require('discord.js');




module.exports = {
    data: new SlashCommandBuilder()
        .setName('joe')
        .setDescription('( ͡° ͜ʖ ͡°)'),
    async execute(interaction) {
        await interaction.reply('mama');
    },
};