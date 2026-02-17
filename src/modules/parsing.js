import Point from "../models/point.js";
import PointCollection from "../models/point_collection.js";

const collectionPoints = new PointCollection();

export function validationSaisiRegex(value) {
    // Expression régulière pour valider le format 'X, Y' (X et Y peuvent être des nombres avec des décimales)
    let regex = /^\s*(-?\d+(\.\d+)?),\s*(-?\d+(\.\d+)?)\s*$/;
    return value.match(regex);
}

export function setPointIntoCollection(x, y) {
    let point = new Point(x,y);
    collectionPoints.addPoint(point);
    console.log(collectionPoints); // To debug: Affiche la collection de points après l'ajout
}