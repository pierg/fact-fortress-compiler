use dep::std;

mod data;

fn concatenate(data: data::Data) -> [u8; data::DATA_SIZE]  {
    let mut result = [0; data::DATA_SIZE];
    let mut cur_i = 0;
    for i in 0..data::D1_SIZE {
        result[cur_i] = data.d1[i] as u8;
        cur_i = cur_i + 1;
    }
    for i in 0..data::D2_SIZE {
        result[cur_i] = data.d2[i] as u8;
        cur_i = cur_i + 1;
    }
    result 
}

