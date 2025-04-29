
<p align="center">
  <img src="assets/capture 5.png"  width="800">
</p>

## Script Binance

Ce script Python est un bot de trading automatique basé sur les moyennes mobiles simples (SMA), exactement comme sur Binance, en gros : 

Le bot regarde deux moyennes de prix : une courte (SMA7) et une longue (SMA25).

- Si la courte est plus basse, il essaie d’acheter un peu en dessous du prix actuel (-0.3%).

- Si la courte est plus haute, il essaie de vendre un peu au-dessus du prix (+0.3%).

### Conditions préalables

- Créer un compte Binance (compte vérifié)
- Acheter un VPS (personnellement je fais tout mes projets sur OVH, donc j'ai pris un VPS OVH Debian)
- Génerer une Clé API & une Clé API Secrète

Voici un exemple de la liste des éléments dont vous avez besoin pour utiliser le script et de la façon de les installer.

### Installation

1. Installer les modules nécessaires

  ```sh
  pip install python-binance pandas ta
  ```

2. Envoie du Script dans le VPS

   ```sh
   scp C:/Users/gaudr/Documents/Binance/binance_bot.py debian@IP_VPS:/home/debian/
   ```

3. Lancer le script

   ```sh
   python3 /home/debian/binance_bot.py
   ```

3. Installer Cron

   ```sh
   sudo apt update
   sudo apt install cron -y
   ```

4. Automatisation du bot avec Cron

   ```sh
   crontab -e
   ```

5. Ajout de cette ligne de commande pour executer le bot toutes les 15 minutes

   ```sh
   */15 * * * * /home/debian/binance-bot-env/bin/python3 /home/debian/binance_bot.py
   ```

6. Attendez 15-30 minutes, et faites cette ligne de commandes pour voir si le script a fait effet

      ```sh
   cat /home/debian/bot.log
   ```

Voilà, grâce au VPS et au script Cron, le Script Trading Binance va tourner en continue 24/24h, et est maintenant automatisé.

---


