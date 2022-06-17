interface LineFlyweight {
  getColor(): string;
  draw(length: number): void;
}

class Line implements LineFlyweight {
  private color: string;
  constructor(c: string) {
    this.color = c;
  }

  public getColor(): string {
    return this.color;
  }

  public draw(length: number): void {
    // draw something
    console.log('drawing ', this.color, ' line in this length', length);
  }
}

class LineFlyweightFactory {
  private pool: Array<LineFlyweight> = [];

  public LineFlyWeightFactory() {
    this.pool = new Array<LineFlyweight>();
  }

  public getLine(color: string): LineFlyweight {
    //check if we've already created a line with this color
    for(let i = 0; i < this.pool.length; i ++) {
      if(this.pool[i].getColor() === color) {
        return this.pool[i];
      }
    }
    // if not, create a new one and save to this pool
    let line = new Line(color);
    this.pool.push(line);
    return line;
  }
}

let factory = new LineFlyweightFactory();
let line = factory.getLine('red');
let line2 = factory.getLine('red');

line.draw(300);
line2.draw(400);

if (line == line2) {
  console.log('line and line2 is same instance');
}