import { Point } from "./point.js";

export class Rectangle {
  constructor(
    public readonly topLeft: Point,
    public readonly width: number,
    public readonly height: number
  ) {
    if (width <= 0) throw new Error("width must be positive");
    if (height <= 0) throw new Error("height must be positive");
  }

  area(): number {
    return this.width * this.height;
  }

  perimeter(): number {
    return 2 * (this.width + this.height);
  }

  contains(point: Point): boolean {
    return (
      point.x >= this.topLeft.x &&
      point.x <= this.topLeft.x + this.width &&
      point.y >= this.topLeft.y &&
      point.y <= this.topLeft.y + this.height
    );
  }

  toString(): string {
    return `Rectangle(${this.topLeft.toString()}, ${this.width}×${this.height})`;
  }
}
