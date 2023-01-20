const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');
var undici = require("undici");
var heroEmbed;
var heroList = [];
var heroes;
var message;

async function getList(){
    var response = await undici.request("https://overfast-api.tekrop.fr/heroes");

    heroes = await response.body.text();

    makeList();
}

function makeList(){
    var heroesJSON = JSON.parse(heroes);
    
    heroesList = [];

    heroesJSON.forEach(H => heroesList.push(H.key));
}

async function getData(name, interaction){
    var heroName = name.toLowerCase();
    var hero;
    await getList().then(() => doRest(heroName, hero, interaction));
}

async function doRest(heroName, hero, interaction){
    var response = await undici.request(`https://overfast-api.tekrop.fr/heroes/${heroName}`);
    hero = await response.body.text();
    var heroJSON = JSON.parse(hero);
    
    if (heroesList.includes(heroName)){
        var role = heroJSON.role;
        var heroRole = role.charAt(0).toUpperCase() + role.slice(1);
    
        heroEmbed = new EmbedBuilder()
            .setColor(0xF7AB05)
            .setTitle(heroJSON.name)
            .setDescription(heroJSON.description)
            .setThumbnail(heroJSON.portrait)
            .setAuthor({ name: heroRole, iconURL: heroJSON.portrait})
            .addFields(
                { name: 'Location:', value: heroJSON.location},
                { name: '\u200B', value: '\u200B' },
                { name: '***Abilities***', value: '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━' },
                { name: "__" + heroJSON.abilities[0].name + "__", value: "*" + heroJSON.abilities[0].description + "*"},
                { name: "__" + heroJSON.abilities[1].name + "__", value: "*" + heroJSON.abilities[1].description + "*"},
                { name: "__" + heroJSON.abilities[2].name + "__", value: "*" + heroJSON.abilities[2].description + "*"},
                { name: "__" + heroJSON.abilities[3].name + "__", value: "*" + heroJSON.abilities[3].description + "*"},
                { name: '\u200B', value: '\u200B' },
            )
            .setImage(heroJSON.portrait)
            .setFooter({ text: "Created by @Menace#2111", iconURL: 'https://i.imgur.com/uTQbX7K.jpg' })
            .setTimestamp();
            
        interaction.reply({ embeds: [heroEmbed] });
    }
    else if (!heroesList.includes(heroName)){
        interaction.reply("⛔ UNABLE TO LOOKUP HERO, INVALID HERO NAME:  `" + interaction.options.getString("name") + "` ⛔\nPlease refer to this example `/hero wrecking-ball`\n**CAPITALIZATION DOES NOT MATTER.**");
    }
}






module.exports = {
    data: new SlashCommandBuilder()
        .setName('hero')
        .setDescription('Prints out all data of a specific hero.')
        .addStringOption(option =>
            option.setName('name')
                .setDescription('Hero name replacing spaces with dashes and excluding punctuation and special characters.')
                .setRequired(true)
            ),
    async execute(interaction) {
        await getData(interaction.options.getString('name'), interaction);
    },
};