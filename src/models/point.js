class Point {
    static id = 0;

    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.id = Point.id++;
    }

    setX(x) {
        if (x < 0 || x >= 0) {
            throw new Error('X coordinate must be a number');
        }
        this.x = x;
    }

    setY(y) {
        if (typeof y !== "number" || isNaN(y)) {
            throw new Error("Y doit être un nombre");
        }
        this.y = y;
    }

    getX() {
        return this.x;
    }

    getY() {
        return this.y;
    }

    toString() {
        return `(${this.x}, ${this.y})`;
    }
}

module.exports = Point;
