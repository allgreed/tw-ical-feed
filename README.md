# tw-ical-feed
See your [due] dates for tasks on a calendar, generates an ics feed 

## Usage
For now go for [dev](#dev)

### Manual integration

There's also the experimental notion of planning.

- add the following to your `.taskrc`:
```
uda.estimate.type=duration
uda.estimate.label=Est
uda.plan.type=date
uda.plan.label=Planned
```

- populate this attribute, example:
```
task mod [id] estimate:15min plan:today+12h
```

And a plan event will be created for that task from today 12:00 to 12:15

## Dev

### Prerequisites
- [nix](https://nixos.org/download.html)
- `direnv` (`nix-env -iA nixpkgs.direnv`)
- [configured direnv shell hook ](https://direnv.net/docs/hook.html)
- some form of `make` (`nix-env -iA nixpkgs.gnumake`)

Hint: if something doesn't work because of missing package please add the package to `default.nix` instead of installing it on your computer. Why solve the problem for one if you can solve the problem for all? ;)

### One-time setup
```
make init
```

### Everything
```
make help
```
