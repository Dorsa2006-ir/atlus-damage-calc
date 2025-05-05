import os
import discord
from discord.ext import commands
from discord.commands import Option

intents = discord.Intents.default()
bot = discord.Bot(intents=intents)

# Mappings
ATTACK_POWER_MAP = {
    "miniscule": 20,
    "light": 40,
    "medium": 80,
    "heavy": 120,
    "severe": 160,
    "colossal": 200
}


ATTACK_MODIFIERS = {
    "none": 1.0,
    "attack down": 0.7,
    "attack up": 1.3,
    "attack up defense down": 1.6,
    "attack down defense up": 0.4
}

CHARGE_MULTIPLIERS = {"yes": 1.5, "no": 1.0}
BATON_MULTIPLIERS = {"none": 1.0, "one": 1.2, "two": 1.4, "three": 1.6}
GUARD_MULTIPLIERS = {"yes": 0.5, "no": 1.0}
AMPS_BOOSTS = {
    "none": 1.0, "boosted": 1.25, "amped": 1.5,
    "boost+amp": 1.75, "full": 2.0
}

def calculate_damage(
    attack_power_label, attack_stat, multihit, defense_stat,
    attack_modifier="none", charge="no", baton="none", guard="no",
    move_bonus=None, amp_boost="none"
):
    # Lowercasing inputs
    attack_power_label = attack_power_label.lower()
    attack_modifier = attack_modifier.lower()
    charge = charge.lower()
    baton = baton.lower()
    guard = guard.lower()
    amp_boost = amp_boost.lower()

    # Default move bonus if not provided
    if move_bonus is None:
        move_bonus = 1.0

    # Validation
    if attack_power_label not in ATTACK_POWER_MAP:
        return f"Invalid attack power: {attack_power_label}"
    if attack_modifier not in ATTACK_MODIFIERS:
        return f"Invalid attack modifier: {attack_modifier}"
    if charge not in CHARGE_MULTIPLIERS or baton not in BATON_MULTIPLIERS or guard not in GUARD_MULTIPLIERS:
        return "Invalid value for charge/baton/guard."
    if amp_boost not in AMPS_BOOSTS:
        return f"Invalid amp/boost value: {amp_boost}"
    if not (1 <= attack_stat <= 99 and 1 <= defense_stat <= 99 and 1 <= multihit <= 99):
        return "Attack, defense, and multihit must be 1–99"

    base_damage = (ATTACK_POWER_MAP[attack_power_label] * attack_stat + multihit) / defense_stat
    multiplier = (
        ATTACK_MODIFIERS[attack_modifier] *
        CHARGE_MULTIPLIERS[charge] *
        BATON_MULTIPLIERS[baton] *
        GUARD_MULTIPLIERS[guard] *
        move_bonus *
        AMPS_BOOSTS[amp_boost]
    )
    final_damage = base_damage * multiplier
    return f"Calculated Damage: {final_damage:.2f}"

@bot.slash_command(name="damage", description="Calculate damage with modifiers")
async def damage(
    ctx: discord.ApplicationContext,
    attack_power: Option(str, "Attack power", choices=list(ATTACK_POWER_MAP.keys())),
    attack_stat: Option(int, "Attack stat (1–99)", min_value=1, max_value=99),
    multihit: Option(int, "Multihit (1–99)", min_value=1, max_value=99),
    defense_stat: Option(int, "Defense stat (1–99)", min_value=1, max_value=99),
    attack_modifier: Option(str, "Attack modifier", choices=list(ATTACK_MODIFIERS.keys()), default="none"),
    charge: Option(str, "Concentrated/Charged?", choices=["yes", "no"], default="no"),
    baton: Option(str, "Baton pass boost", choices=["none", "one", "two", "three"], default="none"),
    guard: Option(str, "Enemy guard?", choices=["yes", "no"], default="no"),
    move_bonus: Option(float, "Move bonus (1.1–2.0)", min_value=1.1, max_value=2.0, required=False),
    amp_boost: Option(str, "Amp/Boost status", choices=list(AMPS_BOOSTS.keys()), default="none")
):
    result = calculate_damage(
        attack_power, attack_stat, multihit, defense_stat,
        attack_modifier, charge, baton, guard, move_bonus, amp_boost
    )
    await ctx.respond(result)

bot.run("MTM2ODY1OTE3MzA0NjQ4NTAzMg.G--P4_.QE0Rt_TuB0hNDfBldTSrg02VatqvJpCdR1Qe3s")
# Run bot using token from environment

