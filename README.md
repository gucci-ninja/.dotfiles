# Introduction

Along with my dotfiles, this will also document how I installed Arch Linux - in caseI have to do it again.
This is my second installation because my first one, for whatever reason, died and I didn't even have my dotfiles backed up to git.

# Step 1 - Booting the ISO
I already have an ISO image of Arch Linux on a USB so I just plugged that in, spammed F2/F3 repeatedly until I saw the boot menu.
Then I selected the option to boot into the USB.

# Step 2 - Mount system
This is actually a bunch of steps but I *usually* do them all at once

```
# To see partitions
fdisk -l
```
My EFI disk is sda1 and the arch one is sda5.

```
# To format sda5
mkfs ext4 -L "Arch Linux" /dev/sda5

# To mount the partition
mount /dev/sda5 /mnt

# Get wifi
wifi-menu

# Install base system
pacstrap /mnt base base-devel vim

# Mount EFI partition
mkdir -p /mnt/boot/efi
mount /dev/sda1 /mnt/boot/efi

# Generate the fstab (I have no clue what this is)
genfstab -p /mnt >> /mnt/etc/fstab
```

# Step 4 - Get out of the USB

```
# Chroot into arch linux
arch-chroot /mnt
```

# Step 5 - Wifi

```
pacman -S networkmanager

# Automatically start it up
systemctl enable NetworkManager
```

# Step 6 - Bootloader
You need something to load your OS each time so get grub.

```
# Download grub
pacman -S grub efibootmgr

# Install grub into HDD
grub-install /dev/sda
ls -l /boot/efi/EFI/arch

# Generate grub config
grub -mkconfig -o /boot/grub/grub.cfg
```

# Step 7 - Set Up Some Boring Things

```
timedatectl set-ntp true

# Set up timezone
ln -sf /usr/share/zoneinfo/Canada/Eastern /etc/localtime

# Set clock
hwclock --systohc

# Also set locale
# First uncomment the Canada locale in /etc/locale.gen
vi /etc/locale.gen
# Generate the locales
locale-gen

# Do this step
mkinitcpio -p linux

# Set the root password
passwd
```

# Step 9 - Unmount

```
umount -R /mnt
reboot
```

Now you can take out the USB.

# Step 10 - Take a break because you've come this far
:sunglasses:

# Step 11 - Users
After rebooting login as root and create a user.

```
useradd -m -g wheel suhavi
psswd suhavi

# Give sudo ability
vim /etc/sudoers
# Uncomment the following line
%wheel ALl=(ALL) ALL
```

# Step 12 - Xorg
This is a graphical server.
```
pacman -S xorg-server xorg-init
# Type startx to start it
```

# Step 13 - Terminal + Shell + Git + VS Code
- fish is a spicy shell
```
pacman -S termite fish git code

# Make fish your default
chsh -l # See all shells
chsh -s fish

# Copy the following to fish config file to make startx run on startup
if status is-login
  if test -z "$DISPLAY" -a $XDG_VTNR = 1
    exec startx -- -keeptty
  end
end

```

# Step 14 - Window MANAGER >:)))))
It's time to get bspwm

```
pacman -S bspwm dmenu sxhkd

# Fonts
pacman -S noto-fonts
# Fonts can be managed at ~/.config/fontconfig/fonts.conf

# Make x server start bspwm
vim ~/xinitrc
# Add the followng
sxhkd &
exec bspwm

# Make termite your default terminal by going into the sxhkdrc file and changing xterm to termite

# Add custom keybinds to sxhkdrc
```

# Step 15 - Sound
I didn't have sound in the beginning.

```
pacman -S alsa-utils
alsamixer -c 0
```

Use the arrow keys and stuff to toggle all sound things on

# Step 16 - Wallpaper
- find a good wallpaper

```
feh --bg-scale wallpaper.jpg

# Edit the following to xinitrc
~/.fehbg &

# Make sure it's before exec bspwm^
```

# Step 17 - Yay
- this will help download AUR things

```
git clone https://aur.archlinux.org/yay.git

cd yay

makepkg -si
```
# Step 18 - Polybar
I actually hate this part

```
yay -S polybar
install -Dm644 /usr/share/doc/polybar/config $HOME/.config/polybar/config
example polybar

# Make a lot of changes to example config

# I was getting unicode errors so
sudo pacman -S ttf-font-awesome

# In polybar config change fonts
font-1 = "Font Awesome 5 Free:style=Regular:size=10;5"
font-2 = "Font Awesome 5 Free:style=Solid:size=10;5"

# Go through all unicode characters in polybar config and replace them with icons from the FA cheatsheet

# Put this line in bspwmrc
polybar main &

```

# Step 19 - Backing Up Your Dotfiles
I'm not trying to lose all my stuff again.

```
# Initialize a git bare repo
git init --bare $HOME/.dotfiles

# Create an alias
alias dotfiles ="git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME"

# Save alias
funcsave dotfiles

# Ignore files you don't want tracked
dotfiles config --local status.showUntrackedFiles no

# Create a github repo called .dotfiles

# dotfiles remote add origin https://github.com/gucci-ninja/.dotfiles
```

# Step 20 - Make your windows look less ugly
Since I have bspwm I don't have a display manager to add GTK themes to. So I have to get lxappearance >:( I feel lied to

```
yay -S lxappearance
sudo pacman -S gtk-engine-murrine adwaita-icon-theme

```

Step 20 was made possible largely due to this reddit post, https://www.reddit.com/r/unixporn/comments/74z2z6/easily_getting_started_with_bspwm_and_polybar/
and I wish I had found it earlier.

# Step 21 - Neofetch
You don't need to do this, it's mostly fo showing off to people. 

```
pacman -S neofetch

# Add the following to fish.config
neofetch

```

Now eveyr time you create a new terminal session you can show off.

# Step 22 - File Manager
- I'm using thunar

# Step ?? - Aliases

# Step 23 - Connecting to Eduroam
- this is too hard and I failed
- luckily it was easy to connect to Mac-WiFi (note the capitals)
- I'll post my wifi config if someone asks

# Step 24 - Bluetooth
```bash
$ pacman -S bluez bluez-utils
$ pacman -S pulseaudio-bluetooth pulseaudio-alsa pavucontrol

systemctl enable bluetooth.service

$ sudo vim etc/bluetooth/main.conf
# add the following line at the end
# this will ensure your bluetooth headphones auto-connect
AutoEnable=true

# make a directory for pulse (you may already have it)
$ mkdir ~/.config/pulse
# copy sample
$ cp /etc/pulse/* ~/.config/pulse/

$ systemctl restart bluetooth

$ bluetoothctl
# you should be in the bluetooth user now
[bluetooth]~ power on
[bluetooth]~ agent on
[bluetooth]~ default-agent
[bluetooth]~ scan on
# at this point you should put your headphones in pairing mode
# they should show up with a mac address
[bluetooth]~ pair 00:00:00:00:00
[bluetooth]~ connect 00:00:00:00:00
# if this part fails run the following in a new terminal
$ pulseaudio --start
# it should connect now
[bluetooth]~ trust 00:00:00:00:00
[bluetooth]~ scan off
[bluetooth]~ exit

# it should connect your headphoens at this point. if you don't hear sound, restart spotify or whatever and it should work
# if it doesn't, open pavucontrol
$ pavucontrol

# this interface will show you your connected devices, make sure it is not on mute and that under configuration tab it says it's connect to ADP SINK or sm dumb
```
