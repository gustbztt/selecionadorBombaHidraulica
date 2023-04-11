$(function resetFrictionalLossFields() {
    $('#reset').click(function () {
        $("#id_material").val(''); //Pipe diameter
        $("#temperatura").val(''); //Pipe length
        $("#vazaoDesejada").val(''); //Kinematic viscosity
        $("#tempoFuncionamento").val(''); //Dynamic viscosity

    });
});

