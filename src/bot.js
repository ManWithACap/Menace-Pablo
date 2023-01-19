const fs = require('fs');
const path = require('path');
const { Client, Collection, Events, GatewayIntentBits, Activity, ActivityType } = require('discord.js');

const { token, clientId, guildId } = require('../config.json')

const client = new Client({ intents: [GatewayIntentBits.Guilds] });




client.commands = new Collection();

const commandsPath = path.join(__dirname, './commands');
const commandFiles = fs.readdirSync(commandsPath).filter(file => file.endsWith('.js'));

for (const file of commandFiles) {
	const filePath = path.join(commandsPath, file);
	const command = require(filePath);
	if ('data' in command && 'execute' in command) {
        console.log(command.data.name);
		client.commands.set(command.data.name, command);
	} else {
		console.log(`[WARNING] The command at ${filePath} is missing a required "data" or "execute" property.`);
	}
}


client.once(Events.ClientReady, c => {

    console.log(`Ready! Logged in as ${c.user.tag}. I'm locked, loaded and ready to rock!!`);

    client.user.setActivity('💞 HoneySelect2Libido DX 💞', { type: ActivityType.Playing });

});


client.on(Events.InteractionCreate, async interaction => {
    if (!interaction.isChatInputCommand()) return;
    
    
    const command = interaction.client.commands.get(interaction.commandName);


    if (!command) {
        console.error(`No command matching ${interaction.commandName} was found.`);
    }

    
    try {
        await command.execute(interaction);
    } catch (error) {
        console.error(error);
        await interaction.reply({ content: `There was an error while executing this command!`, ephemeral: true});
    }
});


client.login(token);