#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>

/**
 * Hilfsfunction, damit man bit verschieben kann.
 * Hier schiebe ich die bits nur links
 * @param uint32_t x: die Zahl ich verschiebe
 * @param int n: die Anzahl der bits die ich verschiebe
 * @return uint32_t: die verschobene Zahl
 */
uint32_t rotate(uint32_t x, int n)
{
    return (x << n) | (x >> (32-n));
}

/**
 * Die QuarterRound Funktion von ChaCha20
 * @param uint32_t *a: Zeiger auf die erste Zahl
 * @param uint32_t *b: Zeiger auf die zweite Zahl
 * @param uint32_t *c: Zeiger auf die dritte Zahl
 * @param uint32_t *d: Zeiger auf die vierte Zahl
 */
void quarterround(uint32_t *a, uint32_t *b, uint32_t *c, uint32_t *d)
{
    // Erste Schritt
    *a = (*a + *b);
    *d = (*d ^ *a);
    *d = rotate(*d,16);

    //Zweite Schritt
    *c = (*c + *d);
    *b = (*b ^ *c);
    *b = rotate(*b,12);

    //Dritte Schritt
    *a = ( *a +*b);
    *d = (*d ^ *a);
    *d = rotate(*d,8);

    // Letzte Schritt
    *c = (*c + *d);
    *b = (*b ^ *c);
    *b = rotate(*b,7);
}

int main(void)
{
    //Gegebene Zahlen
    uint32_t a = 0x00000001;
    uint32_t b = 0x00000000;
    uint32_t c = 0x00000000;
    uint32_t d = 0x00000000;

    printf("Eingang:\n");
    printf(" a = 0x%08" PRIx32 "\n", a); // %08 sorgt dafuer, dass immer 8 Stellen angezeigt werden , PRIx32 sorgt dafuer, dass die Zahl im Hexadezimalformat ausgegeben wird
    printf(" b = 0x%08" PRIx32 "\n", b); 
    printf(" c = 0x%08" PRIx32 "\n", c);
    printf(" d = 0x%08" PRIx32 "\n", d);

    //Erwartete Werte nach manueller Berechnung
    uint32_t expected_a = 0x10000001;
    uint32_t expected_b = 0x80808808;
    uint32_t expected_c = 0x01010110;
    uint32_t expected_d = 0x01000110;

    quarterround(&a, &b, &c, &d);

    printf("\nAusgang (nach QuarterRound):\n");
    printf(" a = 0x%08" PRIx32 "\n", a);
    printf(" b = 0x%08" PRIx32 "\n", b);
    printf(" c = 0x%08" PRIx32 "\n", c);
    printf(" d = 0x%08" PRIx32 "\n", d);

    //Ueberpruefung der Ergebnisse
    if (a == expected_a && b == expected_b && c == expected_c && d == expected_d) {
        printf("\nQuarterRound funktioniert korrekt!\n");
    } else {
        printf("\nQuarterRound funktioniert NICHT korrekt!\n"); 
    }
    
    return 0;
}