use std::fs::File;
use std::io::{BufRead, BufReader};
use std::time::Instant;

fn main() -> std::io::Result<()> {
    let now = Instant::now();

    //let verbose = false;
    let mut total = 0;
    //let file = File::open("src/inp_ex.txt")?;
    //let file = File::open("src/inp_ex_2.txt")?;
    let file = File::open("src/inp.txt")?;
    let reader = BufReader::new(file);

    let digits = vec![("one",1), ("two",2), ("three",3), ("four",4), ("five",5), ("six",6), ("seven",7), ("eight",8), ("nine",9)];
    let digits_rev = vec![("eno",1), ("owt",2), ("eerht",3), ("ruof",4), ("evif",5), ("xis",6), ("neves",7), ("thgie",8), ("enin",9)];

    for line in reader.lines() {
        let l = line?;
        let l_rev = &l.chars().rev().collect::<String>();
        let mut f_d = 0;
        let mut l_d = 0;

        //take the line as chars
        'outer: for (i, c) in l.chars().enumerate() {
            if c.is_ascii_digit() {
                f_d = (c as u8 - b'0') as i32;
                break;
            } else {
                //not a digit, try number table
                for (from, to) in &digits {
                    let substring_end = i + from.len();
                    if substring_end <= l.len() {
                        let substring = &l[i..i + from.len()];
                        //compare from with string slice
                        if substring == *from {
                            f_d = *to;
                            //only one will work, so if we get a hit break
                            break 'outer;
                        }
                    }
                }
            }
        }

        //now do the same thing but with a reversed line and replacements
        'outer: for (i, c) in l.chars().rev().enumerate() {
            if c.is_ascii_digit() {
                l_d = (c as u8 - b'0') as i32;
                break;
            } else {
                //not a digit, try number table
                for (from, to) in &digits_rev {
                    let substring_end = i + from.len();
                    if substring_end <= l.len() {
                        let substring = &l_rev[i..i + from.len()];
                        //compare from with string slice
                        if substring == *from {
                            l_d = *to;
                            //only one will work, so if we get a hit break
                            break 'outer;
                        }
                    }
                }
            }
        }

        //concat digits and add to total
        total += 10*f_d + l_d;
        
    }

    println!("Total is: {}", total);

    let elapsed = now.elapsed();
    println!("Elapsed: {:.2?}", elapsed);

    Ok(())
}