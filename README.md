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

# I was getting unicode errors so
?? FA ??

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









