use std::fs::File;
use std::io::{BufRead, BufReader};
use std::time::Instant;

fn main() -> std::io::Result<()> {
    let now = Instant::now();

    let verbose = false;
    let mut total = 0;
    let mut total2 = 0;
    //let file = File::open("src/inp_ex.txt")?;
    let file = File::open("src/inp.txt")?;
    let reader = BufReader::new(file);

    for line in reader.lines() {
        let l = line?;
        let (id, max_r, max_g, max_b) = parse_line(&l);
        if verbose { println!("{}, {}, {}, {}", id, max_r, max_g, max_b); };
        //add game id to total if game is possible
        if max_r <= 12 && max_g <= 13 && max_b <= 14 {
            total += id;
        }
        //part 2, add game power
        total2 += max_r*max_g*max_b;
    }

    println!("Total is {}", total);
    println!("Total part 2 is {}", total2);

    let elapsed = now.elapsed();
    println!("Elapsed: {:.2?}", elapsed);
    Ok(())
}

fn parse_line(line: &str) -> (i32, i32, i32, i32) {
    //split by colon, get game ID
    let parts: Vec<&str> = line.split(":").collect();
    let tmp: Vec<&str> = parts[0].split_whitespace().collect();
    let game_id: i32 = tmp[1].parse::<i32>().unwrap();
    let mut max_r = 0;
    let mut max_g = 0;
    let mut max_b = 0;

    //get games
    let parts = parts[1].split(";");
    for game in parts {
        //in each game multiple cube color types can be drawn
        let game_parts = game.split(",");
        for game_part in game_parts {
            //final split, number and color
            let cube_parts: Vec<&str> = game_part.trim().split(" ").collect();
            //color
            let tmp = cube_parts[0].parse::<i32>().unwrap();
            match cube_parts[1] {
                "red" => {
                    if tmp > max_r { max_r = tmp };
                },
                "green" => {
                    if tmp > max_g { max_g = tmp };
                },
                "blue" => {
                    if tmp > max_b { max_b = tmp };
                },
                _ => println!("something else!"),
            }
        }
    }

    (game_id, max_r, max_g, max_b)
}