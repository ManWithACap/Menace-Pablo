const { SlashCommandBuilder, InteractionCollector } = require('discord.js');
const { Client, GatewayIntentBits } = require('discord.js');
const { joinVoiceChannel } = require('@discordjs/voice');
const client = new Client({ intents: [GatewayIntentBits.Guilds] });



module.exports = {
    data: new SlashCommandBuilder()
        .setName('join')
        .setDescription('Adds Menace to the voice channel.'),
    async execute(interaction) {
        await new joinVoiceChannel({
            channelId: interaction.guild.members.cache.get(interaction.member.user.id).voice.channelId,
            guildId: '675390519714775060',
            adapterCreator: interaction.guild.voiceAdapterCreator,
        });
        await interaction.reply("I have arrived. <:Blasphemy:1011903353200054302>");
    },
};