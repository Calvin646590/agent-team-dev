export class Point {
  constructor(public readonly x: number, public readonly y: number) {}

  distanceTo(other: Point): number {
    return Math.sqrt(Math.pow(other.x - this.x, 2) + Math.pow(other.y - this.y, 2));
  }

  toString(): string {
    return `Point(${this.x}, ${this.y})`;
  }
}
