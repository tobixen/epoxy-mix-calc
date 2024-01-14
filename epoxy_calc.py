import click

def avg(coll):
    return sum(coll)/len(coll)

def chop_extremes(coll, strip_num):
    coll.sort()
    return coll[strip_num:-strip_num]

def find_midpoint(coll):
    assert(len(coll)>=6)
    coll = chop_extremes(coll, 2)
    return avg(coll)

def find_hardener(tara, base, hardener, tot_weight, adding, part100):
    if type(tara) == list:
        tara = find_midpoint(tara)
    if type(base) == list:
        base = find_midpoint(base) - tara
    if type(tot_weight) == list:
        tot_weight = find_midpoint(tot_weight)
        mass_added = tot_weight-base-tara-hardener
        assert mass_added>0
        click.echo(f"New {adding} added: {mass_added}")
        ## locals()[adding] += foo seems to work when testing interactively in python, but not here.  weird.
        if adding == 'hardener':
            hardener += mass_added
        elif adding == 'base':
            base += mass_added
    hardener_needed = base*part100/100 - hardener
    click.echo(f"tara: {tara:.1f}g")
    click.echo(f"base: {base:.1f}g")
    click.echo(f"hardener: {hardener:.1f}g")
    click.echo(f"more hardener needed: {hardener_needed:.1f}g")
    click.echo(f"total weight needed: {tara+base+hardener+hardener_needed:.1f}g")
    return (tara,base,hardener,hardener_needed)

def interactive_read_numbers(what):
    ret = []
    while True:
        number = click.prompt(f"Enter {what}", default='---')
        if number == '---':
            if len(ret) < 6:
                click.echo("more numbers needed!")
                continue
            break
        try:
            number = float(number)
        except:
            click.echo("Not a number!  Try again")
            continue
        ret.append(number)
    return ret

def interactive():
    part100 = float(click.prompt("How many grams of hardenere is needed for 100g of base"))
    click.echo("measure the tara.  Enter the observed tara at least six times.")
    tara = interactive_read_numbers('tara')
    click.echo("Add base and enter the observed total weight at least six times.")
    base = interactive_read_numbers('total weight base+tara')
    hardener = 0
    what_needed = 'hardener'
    total_weight = None
    while True:
        (tara, base, hardener, hardener_needed) = find_hardener(tara, base, hardener, total_weight, what_needed, part100)
        if hardener_needed<0:
            what_needed = 'base'
            mass_needed = -hardener_needed/part100*100
        else:
            what_needed = 'hardener'
            mass_needed = hardener_needed
        if mass_needed < 0.25:
            return
        click.echo(f"Try to add {mass_needed:.1f}g {what_needed}.  Enter the observed total weight at least six times.")
        total_weight = interactive_read_numbers(f"total weight tara+base+hardener after adding {what_needed}")

if __name__ == '__main__':
    interactive()
