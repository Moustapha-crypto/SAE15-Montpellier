import requests
import time
import json

print("=== SURVEILLANCE DES PARKINGS VOITURES ===")
te = int(input("Temps entre chaque mesure (secondes) : "))
duree = int(input("Durée totale (secondes) : "))

# Création du fichier de surveillance avec encodage UTF-8
chemin = 'C:\\Users\\lenovo\\Desktop\\SAE données\\place_libres_tous_parkings.txt'
f = open(chemin, 'w', encoding='utf-8')
f.write(f"=== SURVEILLANCE DES PARKINGS VOITURES ===\n")
f.write(f"Début : {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
f.write(f"Intervalle : {te} secondes\n")
f.write(f"Durée prévue : {duree} secondes\n")
f.write("="*50 + "\n\n")

temps_debut = time.time()
mesure = 0
interrompu = False

print("\nDémarrage de la surveillance...")
print("Appuyez sur Ctrl+C pour arrêter et sauvegarder\n")

try:
    while time.time() - temps_debut < duree:
        mesure += 1
        heure = time.strftime("%H:%M:%S")
        
        print(f"Mesure {mesure} à {heure}")
        f.write(f"\n=== Mesure {mesure} - {heure} ===\n")
        
        # Récupérer les données
        try:
            reponse = requests.get("https://portail-api-data.montpellier3m.fr/offstreetparking?limit=1000")
            reponse.encoding = 'utf-8'  # Forcer l'encodage UTF-8
            parkings = reponse.json()
            
            # Écrire chaque parking
            for p in parkings:
                try:
                    nom = p['name']['value']
                    libres = p['availableSpotNumber']['value']
                    total = p['totalSpotNumber']['value']
                    f.write(f"{nom} : {libres}/{total} places\n")
                except KeyError:
                    continue
            
            f.flush()  # Force l'écriture sur le disque
            print(f"  ✓ {len(parkings)} parkings enregistrés")
            
        except Exception as e:
            f.write(f"✗ Erreur : {str(e)}\n")
            f.flush()
            print(f"  ✗ Erreur: {e}")
        
        # Attente avec vérification d'interruption
        temps_restant = te
        while temps_restant > 0:
            try:
                time.sleep(1)
                temps_restant -= 1
            except KeyboardInterrupt:
                interrompu = True
                break
        
        if interrompu:
            break

except KeyboardInterrupt:
    interrompu = True

except Exception as e:
    print(f"Erreur inattendue: {e}")
    interrompu = True

finally:
    # ========== FINALISATION ==========
    temps_fin = time.time()
    duree_reelle = temps_fin - temps_debut
    
    f.write("\n" + "="*50 + "\n")
    f.write(f"Fin : {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Durée réelle : {duree_reelle:.1f} secondes\n")
    f.write(f"Nombre de mesures effectuées : {mesure}\n")
    
    if interrompu:
        f.write("Statut : INTERROMPU MANUELLEMENT\n")
    else:
        f.write("Statut : TERMINÉ\n")
    
    f.close()
    
    print(f"\n{'═'*50}")
    print(f"TERMINÉ !")
    print(f"  • {mesure} mesures dans '{chemin}'")
    print(f"  • Durée réelle : {duree_reelle:.1f} secondes")
    
    if interrompu:
        print(f"  • Arrêt manuel à {time.strftime('%H:%M:%S')}")