const Point = require("../src/models/Point.js");

describe("Classe Point", () => {

    test("Création valide d'un point", () => {
        const p = new Point(10, 20);

        expect(p.getX()).toBe(10);
        expect(p.getY()).toBe(20);
    });

});
