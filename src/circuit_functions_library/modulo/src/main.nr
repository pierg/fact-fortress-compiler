mod data;

fn main(private : data::Private,    // Data to be verified and processed.
        ) -> pub [u8;8] {
        // ) -> pub u8 {

    constrain private.data.d2[0] == 24;

    let mut result = [0;8];

    let max_size = 4 as u8;

    for i in 0..8{
        // DOES NOT WORK: result=[0,0,0,0]
        // let mut i_mod = (i as u8 % 2 as u8) as u8;
        // result[i] = i_mod;
        // coj = (i as u8) % (1 as u8);
        // DEFINE MODULO
        let mut floor = (i as u8) / max_size;
        let mut mult = max_size * floor;
        let mut i_mod = i - mult as Field;
        result[i_mod] = 3 as u8;
    }
    result
} 
