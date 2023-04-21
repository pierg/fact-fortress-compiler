from shared import Aggregator


D1_SIZE = 8
D1_SHAPE_0 = 2
D1_SHAPE_1 = 4
D1_TYPE = "u8"
D2_SIZE = 2
D2_SHAPE_0 = 2
D2_SHAPE_1 = 1
D2_TYPE = "u8"
DOT_TYPE = f"u{2*int(D1_TYPE[1])}"
DIV_TYPE = f"u{4*int(D1_TYPE[1])}"

print(DOT_TYPE)
print(DIV_TYPE)


def generate_dot_product_multi(
    data_1_name: str,
    data_1_info: dict,
    data_2_name: str,
    data_2: dict,
    aggregator: Aggregator,
) -> str:
    DOT_TYPE = f"u{2*int(D1_TYPE[1])}"
    DIV_TYPE = f"u{4*int(D1_TYPE[1])}"
    D1_SHAPE_1 = data_1_info["shape"][1]
    D1_SHAPE_0 = data_1_info["shape"][0]

    # Noir code generation
    noir_code = f"""fn dot_product(x : [{D1_TYPE}; data::{data_2_name}_SHAPE_0], y : [{D1_TYPE}; data::{data_2_name}_SHAPE_0]) -> {DOT_TYPE} {{
        let mut result = 0;
        for i in 0..{D2_SHAPE_0} {{
            result = result + (x[i] as {DOT_TYPE} * y[i] as {DOT_TYPE});
        }}
        result
    }}

    fn unroll_and_compute(x : [{D1_TYPE}; data::{data_2_name}_SIZE], 
                        y : [{D1_TYPE}; data::{data_2_name}_SHAPE_0]) -> [{DOT_TYPE}; {D1_SHAPE_1}] {{
        let mut result = [0; {D1_SHAPE_1}];
        for i in 0..{(D1_SHAPE_1)} {{
            let start = i * {D1_SHAPE_0} as Field;
            let end = start + {D1_SHAPE_0} as Field;
            let mut x_slice = [0; {D1_SHAPE_0}];
            for j in start..end {{
                let mut slice_index = j - start;
                x_slice[slice_index] = x[j] as {D1_TYPE};
                result[i] = dot_product(x_slice, y);
            }}
        }}
        result
    }}

    fn average(x: [{DOT_TYPE}; {D1_SHAPE_1}]) -> {DOT_TYPE} {{
        let mut sum = 0;
        for i in 0..{D1_SHAPE_1} as Field {{
            sum += x[i] as {DIV_TYPE};
        }}
        let avg = sum / {D1_SHAPE_1} as {DIV_TYPE};
        avg as {DOT_TYPE}
    }}"""

    return noir_code
